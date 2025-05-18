import subprocess

from setuptools import Command, find_packages, setup


class FormatCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(["black", "."], check=True)


class RemoveUnusedImports(Command):
    description = "Remove unused imports"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(
            [
                "autoflake",
                "--verbose",
                "--recursive",
                "--remove-all-unused-imports",
                "--in-place",
                ".",
            ],
            check=True,
        )


class CorrectImports(Command):
    description = "Correct imports"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(
            ["isort", "--verbose", "--overwrite-in-place", "--recursive", "."],
            check=True,
        )


setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    cmdclass={
        "format": FormatCommand,
        "remove_unused_imports": RemoveUnusedImports,
        "correct_imports": CorrectImports,
    },
)
