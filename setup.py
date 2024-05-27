import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="ShockFinder",
    version="7.4.8",
    author="Junxiang H. & C. B. Singh",
    author_email="huangjunxiang@mail.ynu.edu.cn",
    description="ShockFinder is an interactive scientic simulation data analysis software based on python and supports multi-process, multi-mode, I/O access and drawing.",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/wacmkxiaoyi/Shockfinder", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
    install_requires=[
        'matplotlib',
        'numpy',
        'scipy',
        'lmfit',
        'tkinter',
        'XME',
        'XenonUI'
    ],
)