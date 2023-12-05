# PyTorch
<!-- Extracted and adapted from  https://en.wikipedia.org/wiki/PyTorch (2023/12/04) -->

**PyTorch** is a machine learning framework based on the Torch library, used for applications such as computer vision and natural language processing, originally developed by Meta AI and now part of the Linux Foundation umbrella.
It is free and open-source software released under the modified BSD license.
Although the Python interface is more polished and the primary focus of development, PyTorch also has a C++ interface.

A number of pieces of deep learning software are built on top of PyTorch, including Tesla Autopilot, Uber's Pyro, Hugging Face's Transformers, PyTorch
Lightning, and Catalyst.

PyTorch provides two high-level features:

- Tensor computing (like NumPy) with strong acceleration via graphics processing units (GPU)
- Deep neural networks built on a tape-based automatic differentiation system

## History

Meta (formerly known as Facebook) operates both *PyTorch* and *Convolutional Architecture for Fast Feature Embedding* (Caffe2), but models defined by the two frameworks were mutually incompatible.
The Open Neural Network Exchange (ONNX) project was created by Meta and Microsoft in September 2017 for converting models between frameworks.
Caffe2 was merged into PyTorch at the end of March 2018.
In September 2022, Meta announced that *PyTorch* would be governed by PyTorch Foundation, a newly createdindependent organizationa subsidiary of Linux Foundation.

PyTorch 2.0 was released on 15 March 2023.

## PyTorch tensors

PyTorch defines a class called Tensor (`torch.Tensor`) to store and operate on homogeneous multidimensional rectangular arrays of numbers.
PyTorch Tensors are similar to NumPy Arrays, but can also be operated on a CUDA-capable NVIDIA GPU.
PyTorch has also been developing support for other GPU platforms, for example, AMD's ROCm and Apple's Metal Framework.

PyTorch supports various sub-types of Tensors.

Note that the term "tensor" here does not carry the same meaning as tensor in mathematics or physics.
The meaning of the word in machine learning is only tangentially related to its original meaning as a certain kind of object in linear algebra.

## PyTorch neural networks

PyTorch defines a class called nn (`torch.nn`) to describe neural networks and to support training.