"""Read-only inventory and structural audit. No training or source mutation."""
from pathlib import Path
import csv
import hashlib
import json
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'High-resolution-AI-Data-Center-Training-Workloads-Dataset_FigShare'
records = []
groups = defaultdict(list)
for p in sorted(DATA.rglob('*')):
    if not p.is_file():
        continue
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    rec = dict(path=str(p.relative_to(DATA)), bytes=p.stat().st_size, sha256=digest)
    if p.suffix.lower() == '.csv':
        parts = p.relative_to(DATA).parts
        rec.update(platform=parts[0], workload=parts[1], configuration=p.stem)
        # HWiNFO exports contain legacy single-byte degree symbols.
        encoding = 'utf-8-sig' if parts[0] == 'Node_Dataset' else 'cp1252'
        with p.open(encoding=encoding, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rec['columns'] = header
            rec['duplicate_column_names'] = [k for k,v in Counter(header).items() if v > 1]
            selected = [i for i,c in enumerate(header) if c in ('GPU Power [W]', 'GPU Core Load [%]') or c.endswith('_power_W') or c.endswith('_utilization_percent')]
            blank = Counter()
            bad_width = 0
            rows = 0
            first = last = None
            seen_times = set()
            repeated_times = 0
            for row in reader:
                rows += 1
                bad_width += len(row) != len(header)
                timestamp = tuple(row[:2]) if parts[0] != 'Node_Dataset' else tuple(row[:1])
                first = timestamp if first is None else first
                last = timestamp
                repeated_times += timestamp in seen_times
                seen_times.add(timestamp)
                for i in selected:
                    if i >= len(row) or not row[i].strip():
                        blank[header[i]] += 1
            rec.update(rows=rows, malformed_width_rows=bad_width, first_time=first, last_time=last,
                       repeated_timestamp_rows=repeated_times, selected_columns=[header[i] for i in selected],
                       selected_blank_counts=dict(blank), encoding=encoding)
        groups[digest].append(rec['path'])
    records.append(rec)
duplicates = [v for v in groups.values() if len(v)>1]
csv_records = [r for r in records if 'rows' in r]
counts = Counter((r['platform'],r['workload']) for r in csv_records)
unique_counts = Counter()
seen = set()
for r in csv_records:
    if r['sha256'] not in seen:
        unique_counts[(r['platform'],r['workload'])] += 1
        seen.add(r['sha256'])
summary = dict(files=len(records), csv_files=len(csv_records), unique_csv_hashes=len(groups),
               rows_across_files=sum(r['rows'] for r in csv_records),
               rows_unique_hashes=sum(next(r['rows'] for r in csv_records if r['sha256']==h) for h in groups),
               duplicate_groups=duplicates,
               category_counts=[dict(platform=k[0],workload=k[1],files=v,unique_hashes=unique_counts[k]) for k,v in counts.items()],
               malformed_width_rows=sum(r['malformed_width_rows'] for r in csv_records),
               files_with_repeated_timestamps=sum(bool(r['repeated_timestamp_rows']) for r in csv_records))
(ROOT/'docs/dataset-inventory.json').write_text(json.dumps(dict(summary=summary,files=records),indent=2))
print(json.dumps(summary,indent=2))
