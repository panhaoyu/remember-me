import setuptools

with open('README.md', mode='r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='remember-me',
    version='0.0.1',
    author='wolfpan',
    author_email='haoyupan@aliyun.com',
    description='A python backend of remembering words.',
    long_description=long_description,
    url='https://github.com/panhaoyu/remember-me',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ]
)
