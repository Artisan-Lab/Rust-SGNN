#Safe Rust Code Recommendation Based on
Siamese Graph Neural Network

This repo provides an implementation of the SGNN(Siamese Graph Neural Network) for safe Rust Recommendation .

## Dependency Library

The SGNN is written using Pytorch 1.10.2 in Python 3.9.4. You can install the dependencies by running:

```
pip install -r requirements.txt
```

## Model Implementation

The SGNN model is implemented in `model.py`. Bipartite Graph Match is implemented  in baseline.py. Gemini is implemented  in Gemini.py.

Run the following code to train the model:

```
python model.py
```

After training, run the following code to evaluate the model:

```
python consume_time.py
```