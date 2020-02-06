from setuptools import setup

setup(
    name="Graph",
    packages=["orangegraph"],
    package_data={"orangegraph": ["icons/*.svg"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Console",
        "Environment :: Plugins",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
    ],
    entry_points={"orange.widgets": "Graph = orangegraph"},
)
