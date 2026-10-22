# ⚖️ Licensing, Copyright, and Competition Data Terms

## 1. Source Code License
The custom Python source code, feature engineering scripts, model architectures, validation pipelines, and documentation developed in this repository are released under the **MIT License**:

```text
MIT License

Copyright (c) 2026 Planet Hunters ML Project Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 2. Competition Dataset Terms & Restrictions
- **Dataset Origin:** The photometric starlight time-series arrays (`train_flux.npy`, `test_flux.npy`), centroid arrays (`train_centroid.npy`, `test_centroid.npy`), and metadata CSVs were provided as part of **ML Challenge Hack4Hack 2026 — Round 1: Planet Hunters**.
- **Distribution Restrictions:** In accordance with competition rules and academic integrity standards, raw competition datasets (`data/raw/*.npy`, `data/raw/*.csv`) and processed feature matrices (`data/processed/*.parquet`) are excluded from public version control via `.gitignore`.
- **Intended Use:** The data is proprietary to the Hack4Hack 2026 challenge organizers and is licensed exclusively for participant model training and evaluation within the competition.
- **Competition Rules & Publication Timing Notice:** Under Section 7 of the official rules, *"Sharing code, predictions or labels between teams is not allowed and leads to disqualification."* To preserve competition integrity, this repository must remain private and must not be published or shared publicly until official Round 1 evaluation has concluded or explicit organizer permission is granted. Open-source licensing applies strictly to the original pipeline architecture after the conclusion of the challenge.

---

## 3. Third-Party Library Licenses
This project incorporates open-source libraries that retain their respective licenses:
- **NumPy, SciPy, Pandas, Scikit-learn:** BSD Licenses
- **LightGBM:** MIT License
- **Matplotlib & Seaborn:** PSF / BSD Licenses
- **PyArrow:** Apache 2.0 License
- **Astropy:** BSD 3-Clause License
