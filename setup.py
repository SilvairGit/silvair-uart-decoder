from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="silvair-uart-decoder",
    version="0.1.3",
    packages=find_packages(),
    license='MIT',
    entry_points={
        "console_scripts": [
            "silvair-uart-decoder=silvair_uart_decoder.main:main",
            "generate_uart_decoder_extension=silvair_uart_decoder.main:generate_saleae_extension"
        ]
    },
    url='https://github.com/SilvairGit/silvair-uart-decoder',
    include_package_data=True,
    author="Silvair",
    author_email="support@silvair.com",
    description="Tool for decoding Silvair UART protocol.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["construct", "crcmod"],
    tests_require=["pytest"],
)
