"""
A module for obtaining repo readme and language data from the github API.

Before using this module, read through it, and follow the instructions marked
TODO.

After doing so, run it like this:

    python acquire.py

To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = [
    "abuanwar072/Flutter-Responsive-Admin-Panel-or-Dashboard",
    "pallupz/covid-vaccine-booking", "goharbor/harbor", "public-apis/public-apis",
    "jwasham/coding-interview-university", "DIGITALCRIMINAL/OnlyFans",
    "vinta/awesome-python", "jlevy/the-art-of-command-line", "dogecoin/dogecoin",
    "phamdinhkhanh/vnquant", "audacity/audacity", "Uniswap/uniswap-v3-periphery",
    "swar/Swar-Chia-Plot-Manager", "flutter/flutter", "streamich/react-use",
    "dynamicwebpaige/thinking-in-data", "forem/forem", "Azure/counterfit",
    " Uniswap / uniswap-v3-core", "ionic-team/ionic-framework", "thedevdojo/wave",
    "angular/angular-cli", "benawad/dogehouse", "plausible/analytics",
    "shmykelsa/AAAD", "onimur/onimur", "rossjrw/rossjrw", "garimasingh128/garimasingh128",
    "DenverCoder1/DenverCoder1", "serverless/serverless", "ramitsurana/awesome-kubernetes",
    "aws/aws-cli", "kubernetes-sigs/kubespray",
    'ansible/ansible',
 'TensorSpeech/TensorFlowTTS',
 'plurals/pluralize',
 'vczh/tinymoe',
 'RHVoice/RHVoice',
 'wapmorgan/Morphos',
 'ChenYCL/chrome-extension-udemy-translate',
 'botupdate/botupdate',
 'VinAIResearch/BERTweet',
 'opencog/link-grammar',
 'makerbase-mks/MKS-TFT',
 'google-research-datasets/wiki-reading',
 'davidsbatista/NER-datasets',
 'words/moby',
 'quadrismegistus/prosodic',
 'libindic/indic-trans',
 'wooorm/parse-english',
 'pannous/english-script',
 'frcchang/zpar',
 'hechoendrupal/drupal-console-en',
 'speechio/BigCiDian',
 'godlytalias/Bible-Database',
 'IlyaGusev/rnnmorph',
 'asweigart/simple-turtle-tutorial-for-python',
 'zacanger/profane-words',
 'kavgan/phrase-at-scale',
 'deep-diver/EN-FR-MLT-tensorflow',
 'ElvisQin/ProjectEnglish',
 'jmsv/ety-python',
 'wapmorgan/TimeParser',
 'vim-scripts/LanguageTool',
 'csebuetnlp/banglanmt',
 'SadaqaWorks/Word-By-Word-Quran-Android',
 'PDKT-Team/ctf',
 'mozilla/language-mapping-list',
 'surfinzap/typopo',
 'adlawson/nodejs-langs',
 'Kyubyong/neural_tokenizer',
 'bikenik/Anki_Templates',
 'scriptin/jmdict-simplified',
 'rust-lang-cn/english-chinese-glossary-of-rust',
 'msg-systems/coreferee',
 'davidmfoley/storevil',
 'chadkeck/Natural-Language-Clock',
 'gtarawneh/languagetool-sublime',
 'vilic/a-plus-dictionary',
 'stefantruehl/research-proposal-template',
 'harsh19/Shakespearizing-Modern-English',
 'vanderlee/php-sentence',
 'adetuyiTolu/Language_Time',
 'panda-lang/light',
 'thomhastings/mimikatz-en',
 'dchest/stemmer',
 'google-research-datasets/RxR',
 'chrisjbryant/lmgec-lite',
 'amrsaeedhosny/countries',
 'thomascgray/NooNooFluentRegex',
 'cijic/phpmorphy',
 'notAI-tech/DeepTranslit',
 'AnotherTest/-English',
 'narze/toSkoy',
 'gertd/go-pluralize',
 'binarybottle/engram',
 'pcjbird/fbCharm',
 'echen/unsupervised-language-identification',
 'libindic/soundex',
 'jpaya17/englishisfun',
 'purvanshi/isolvemath',
 'logue/MabiPack',
 'javadev/moneytostr-russian',
 'ddmcdonald/sparser',
 'haliaeetus/iso-639',
 'kariminf/jslingua',
 'mikahama/uralicNLP',
 'wietsedv/gpt2-recycle',
 'rubyworks/english',
 'jan-Lope/Toki_Pona_lessons_English',
 'noops-challenge/wordbot',
 'elliotchance/bento',
 'IINemo/isanlp',
 'matbahasa/TALPCo',
 'rothos/lexitron',
 'PanderMusubi/locale-en-nl',
 'words/ap-style-title-case',
 'RienNeVaPlus/human-id',
 'sharad461/nepali-translator',
 'carlosbrando/custom_resource_name',
 'dlang-tour/english',
 'danakt/spell-checker.js',
 'words/wiktionary',
 'ARIA-VALUSPA/AVP',
 'words/similar-english-words',
 'IBM/MAX-News-Text-Generator',
 'wapmorgan/yii2-inflection',
 'RightCapitalHQ/chinese-style-guide',
 'SpongeBob-222/gomoku',
 'onlyphantom/elang',
 'cofface/superrs-kitchen',
 'rameshjes/Semantic-Textual-Similarity',
 'tomasz-oponowicz/spoken_language_dataset'


]

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        if "language" not in repo_info:
            raise Exception(
                "'language' key not round in response\n{}".format(json.dumps(repo_info))
            )
        return repo_info["language"]
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = ""
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)
