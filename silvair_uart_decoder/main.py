import argparse
import logging
import sys
import shutil
import pathlib

from .input_converters import get_converter, UARTProtocolFrameValidator, ValidationResult
from .uart_protocol.parsers import CommandCode, CommandParamParser


def generate_saleae_extension(argv=None):
    assert argv or sys.argv[1:], "provide path to directory when extension folder should be created"

    dir_of_extension = pathlib.Path(argv or sys.argv[1]).resolve().joinpath("SilvairUARTDecoder")
    pathlib.Path.mkdir(dir_of_extension, exist_ok=True)

    source_path = pathlib.Path(__file__).resolve().parent

    extension_dir = dir_of_extension.joinpath("UARTDecoderExtension.py")
    shutil.copyfile(f"{source_path}/LogicExtension/source_template/SilvairUARTExtension.py_template",
                    str(extension_dir))
    shutil.copyfile(f"{source_path}/LogicExtension/extension.json",
                    dir_of_extension.joinpath("extension.json"))

    with open(str(extension_dir), 'r') as outfile:
        saved_file = outfile.read()
    with open(str(extension_dir), 'w') as outfile:
        outfile.write("import sys")
        outfile.write("\n\n")
        for env_variable in sys.path:
            outfile.write(f"sys.path.append(\"{pathlib.Path(env_variable).as_posix()}\")")
            outfile.write("\n")

        outfile.write("\n")
        outfile.write(saved_file)
    print("Success!")


def main(argv=None):
    command_param_parser = CommandParamParser()
    validator = UARTProtocolFrameValidator()

    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)

    arg_parser = argparse.ArgumentParser(description="UART-protocol decoder")
    arg_parser.add_argument("-f", "--format-converter", default="default", help="Input format converter")
    arg_parser.add_argument("-O", "--output-file", help="Output file path")
    arg_parser.add_argument("input_file", metavar="INPUT_FILE", help="Input file path")

    args = arg_parser.parse_args(argv or sys.argv[1:])

    format_converter = get_converter(args.format_converter, args.input_file, logger)
    if format_converter is None:
        logger.error("Invalid input format converter: `{}`".format(args.format_converter))
        sys.exit(1)

    if args.output_file:
        logger.addHandler(logging.FileHandler(args.output_file, "w"))

    for frame in sorted(format_converter.convert(), key=lambda f: f.timestamp):

        if validator.validate(frame) != ValidationResult.VALID:
            logger.warning("Invalid frame: (%s)", frame)
            continue

        command = CommandCode(frame.command)
        output_line = "{:0<14} [{}] {:30}".format(frame.timestamp, frame.label, command.name)

        if frame.data:
            output_line += command_param_parser.parse(command, frame.data)

        logger.info(output_line)


if __name__ == "__main__":
    main()
