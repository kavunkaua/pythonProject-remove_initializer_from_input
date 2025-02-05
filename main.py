import onnx
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input model")
    parser.add_argument("--output", required=True, help="output model")
    args = parser.parse_args()
    return args


def remove_initializer_from_input():
    inputmodel = "models/TrophNet-v9.onnx"
    model = onnx.load(inputmodel)
    if model.ir_version < 4:
        print(
            'Model with ir_version below 4 requires to include initilizer in graph input'
        )
        return

    inputs = model.graph.input
    name_to_input = {}
    for input in inputs:
        name_to_input[input.name] = input

    for initializer in model.graph.initializer:
        if initializer.name in name_to_input:
            inputs.remove(name_to_input[initializer.name])

    outputmodel = "models/TrophNet-v9_corrected.onnx"
    onnx.save(model, outputmodel)


if __name__ == '__main__':
    remove_initializer_from_input()

