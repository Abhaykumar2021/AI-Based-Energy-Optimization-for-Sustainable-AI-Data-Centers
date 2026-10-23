# GPU Workload Analysis for Sustainable AI Data Centers

An Electrical and Electronics Engineering research project studying how AI workloads relate to electrical power, thermal behavior, and cooling demand.

The long-term goal is to build and validate a software model of data-center cooling, then investigate control strategies that balance cooling electricity, water use, and thermal safety. Our first checkpoint focuses on understanding GPU workload measurements before developing that cooling model.

## First checkpoint

**Research question:** Can GPU power consumption and utilization distinguish documented AI training workload categories on recordings the classifier has never seen?

The proposed initial experiment uses recordings from a single GPU type, the NVIDIA RTX 3060, with five workload categories:

- Feature forecasting
- Image captioning
- Image classification
- Reinforcement learning
- Text generation

Inputs are measured GPU power in watts and GPU utilization in percent. The output is a predicted workload category. We will also test whether summaries of recent measurements improve classification.

The original idea included idle, inference, and training classification. The supplied dataset documents training workloads; verified labels for those three execution modes have not been established. The final task and inclusion criteria will be frozen after the remaining data-quality checks.

## Dataset

We use the **High-resolution AI Data Center Training Workloads Dataset** by Ahmed Abdelaziz Elsayed, Abdullah Azhar Al-Obaidi, and Hany E. Z. Farag.

- [Original dataset and persistent identifier](https://doi.org/10.6084/m9.figshare.31654879)
- [Associated Scientific Data paper](https://doi.org/10.1038/s41597-026-07496-6)
- [Authors' repository](https://github.com/Ahmed-Elsayed95/High-resolution-AI-Data-Center-Training-Workloads-Dataset)

Our local structural audit found:

| Dataset portion | Hardware | Distinct CSV recordings | Recorded rows across distinct files |
| --- | --- | ---: | ---: |
| Single machine | RTX 3060 | 40 | 403,334 |
| Multi-GPU nodes | Eight H100 or eight B200 GPUs per node | 32 | 1,440,000 |
| Total | | 72 | 1,843,334 |

There are 95 CSV paths because reference recordings recur in different parameter-study folders. SHA-256 checks identified 72 byte-distinct CSV files. Byte-distinct files are candidate sessions, not proof of statistical independence. A multi-GPU row includes measurements for eight GPUs belonging to the same run.

The node recordings cover diffusion image generation and LLM training. They may support a separate within-hardware experiment later. We will avoid mixing hardware in a way that lets a classifier recognize GPU type instead of workload.

## Experimental workflow

1. Audit provenance, licenses, numeric validity, timestamps, units, and sensor update behavior.
2. Preserve raw files and create a manifest identifying unique recordings and documented labels.
3. Freeze the task and split whole recording groups into development and held-out test sets. Keep duplicate copies and GPUs from the same run together.
4. Explore development data to understand distributions and overlap between workload categories.
5. Compare a majority-class baseline, logistic regression, a shallow decision tree, and random forest.
6. Compare power-only, utilization-only, combined, and causal temporal-window features.
7. Tune within grouped development folds, then evaluate the selected pipeline on the held-out test set.
8. Report macro-F1, per-class precision/recall/F1, confusion matrices, run-level variability, errors, and limitations.

All learned preprocessing must be fitted on training data only. Windows must not cross split boundaries. We will report negative or inconclusive results as well as improvements.

## Current progress

**Completed:** concept review, initial literature/dataset review, file inventory, checksums, duplicate detection, and structural CSV checks.

**Pending:** license reconciliation, deeper numeric/timing checks, final task definition, grouped splits, exploratory analysis, model training, and evaluation.

No classifiers have been trained and no classification performance or cooling savings have been demonstrated. The audit identified repeated timestamps in three recordings, duplicate column names in single-machine exports, and missing node CPU-power fields. These require explicit handling or documented limitations.

## Tools

The current inventory script uses Python's standard library. The proposed experiment stack is:

| Tool | Purpose |
| --- | --- |
| Python | Data processing and reproducible experiments |
| pandas and NumPy | Validation, preparation, and numerical analysis |
| scikit-learn | Classifiers, pipelines, grouped validation, and metrics |
| Matplotlib and Seaborn | Research plots and error visualization |
| Jupyter | Exploratory analysis and explanatory notebooks |
| Git | Code and documentation version history |

The ML environment and dependency versions have not yet been pinned. The initial experiment is designed for an ordinary laptop without purchasing a GPU or running large AI training jobs.

## Run the existing audit

With Python 3 available, run from the repository root:

```bash
python3 scripts/audit_dataset.py
```

The script expects the extracted source folder named `High-resolution-AI-Data-Center-Training-Workloads-Dataset_FigShare` beside this README. It reads source files without changing them and writes `docs/dataset-inventory.json`. Create the output directory first if it is absent:

```bash
mkdir -p docs
```

The audit inventories files, computes hashes, counts CSV rows, checks row widths and repeated timestamp keys, and records selected blank fields. It does not establish sensor accuracy or complete the remaining quality checks.

## Project layout

```text
README.md
AGENTS.md                      Project working and research-integrity instructions
scripts/
  audit_dataset.py             Existing read-only source-data audit
High-resolution-AI-Data-Center-Training-Workloads-Dataset_FigShare/
                               Original extracted dataset and supplied metadata
docs/                          Locally maintained records; currently Git-ignored
  project-plan.md              Planned/executed steps and decisions
  dataset-audit.md             Initial findings and limitations
  dataset-inventory.json       Generated file provenance and structural checks
  sources-and-ethics.md        Source, license, and ethical-use register
  prompt-log.md                User request history
  response-summary-log.md      Assistant outcome summaries
```

The local documentation files are maintained during project work. They may be absent from a fresh clone because `/docs/` is currently ignored by Git.

## Citation, ethical use, and reproducibility

Citation and ethical use are highest-priority project requirements. Cite the original dataset and associated paper when reporting research based on them, and attribute reused code and methods. Record versions, checksums, preprocessing decisions, exclusions, labels, split manifests, and experiment settings.

The downloaded README and LICENSE state **CC BY-NC-ND 4.0**. An earlier review observed a different license on the Figshare listing. This discrepancy remains unresolved. Do not assume unrestricted reuse or publish processed traces before establishing the applicable permissions. Dataset terms are separate from any license for original project code; this repository does not grant additional rights to third-party material.

Preserve raw measurements and distinguish them from derived quantities, synthetic data, assumptions, and experimental results. AI assistance has been used for planning, audit code, and documentation. Record material assistance and follow institutional or submission-venue disclosure requirements. AI-generated text or labels do not substitute for verified evidence.

## Connection to the larger cooling project

This checkpoint develops the workload-data pipeline and tests what GPU power and utilization reveal about workload behavior. Later stages will require a validated power-to-heat and cooling model, resource accounting, and constrained control experiments. Workload classification alone does not demonstrate reductions in cooling energy or water consumption.
