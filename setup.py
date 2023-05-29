from setuptools import setup, find_packages

setup(
    name="pyaclink",  # 包的名称
    version="1.0",  # 包的版本
    author="Cody Gu",
    author_email="cody23333@gmail.com",
    description="Communication library for ACFly A9",  # 简单描述
    url="https://opendrone.tech/",  # 项目主页
    packages=find_packages(),  # 需要打包的模块
    install_requires=[
        "docutils>=0.3",
        "pyserial",
    ],  # 依赖的其他包
    classifiers=[  # 分类信息
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
)
