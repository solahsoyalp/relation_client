import os
import re
from setuptools import setup, find_packages

# このファイルのディレクトリを取得
here = os.path.abspath(os.path.dirname(__file__))

# バージョン情報を取得
with open(os.path.join(here, 'relation_client', '__init__.py'), 'r', encoding='utf-8') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError('Version information not found')

# README.mdを読み込む
with open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='relation-client',
    version=version,
    description='Re:lation API Python クライアントライブラリ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='solah soyalp',
    author_email='solah.soyalp@gmail.com',
    url='https://github.com/solahsoyalp/relation_client',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'requests>=2.25.0',
        'pytz',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    project_urls={
        'Bug Reports': 'https://github.com/solahsoyalp/relation_client/issues',
        'Source': 'https://github.com/solahsoyalp/relation_client',
    },
    include_package_data=True,
) 