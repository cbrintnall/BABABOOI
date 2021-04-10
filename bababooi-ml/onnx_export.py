#!/usr/bin/env python3
import argparse

import torch

from models import DummyModel


def get_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--checkpoint', help='Path to a model checkpoint.')
    parser.add_argument('-o', '--out', default='model.onnx', help='ONNX write path')
    parser.add_argument('-t', '--type', choices=['dummy'], default='dummy', help='Type of model to export.')
    return parser.parse_args()


def main(args):
    if args.type == 'dummy':
        model = DummyModel.load_from_checkpoint(args.checkpoint)
    else:
        raise ValueError(f'Model type {args.type} not supported.')

    sample = torch.rand(1, 1, 256, 256)
    model.to_onnx(args.out, sample, export_params=True)


if __name__ == '__main__':
    args = get_args()
    main(args)
