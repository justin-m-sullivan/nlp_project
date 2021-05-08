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

REPOS = ['ansible/ansible',
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
 'tomasz-oponowicz/spoken_language_dataset', 'SuzanaK/english_synonyms_antonyms_list',
 'shenhuanet/Ocr-android',
 'Vedenin/code-for-learning-languages',
 'musicamecclesiae/English-Hymns',
 'anuragk240/Speech-to-Sign-Language-Translator',
 'derintelligence/en-az-parallel-corpus',
 'chaira19/Hindi-DateTime-Parser',
 'dhvani-tts/dhvani-tts',
 'UniversalDependencies/UD_English-ESL',
 'dolanskurd/kurdish',
 'crossbowerbt/prolog-talk',
 'shvmshukla/Machine-Translation-Hindi-to-english-',
 'IBM/MAX-Review-Text-Generator',
 'jonschlinkert/diacritics-map',
 'AndriesSHP/Gellish',
 'HoldOffHunger/convert-british-to-american-spellings',
 'vipul-khatana/Hinglish-Sentiment-Analysis',
 'hjian42/Natural-Language-Processing-Nanodegree',
 'oligoglot/theedhum-nandrum',
 'mageplaza/magento-2-italian-language-pack',
 'dan1wang/jsonbook-builder',
 'brentsnook/numerouno',
 'aishek/js-countdown',
 'zoomio/tagify',
 'Kaosam/HTBWriteups',
 'openlanguageprofiles/olp-en-cefrj',
 'ivanovsaleksejs/NumToText',
 'preranas20/Emotion-Detection-in-Speech',
 'freeduke33/rerap2',
 'germanattanasio/professor-languo',
 'jonschlinkert/alphabet',
 'citiususc/SimpleNLG-ES',
 'fizyk/sfForkedDoctrineApplyPlugin',
 'hci-lab/LearningMetersPoems',
 'willettk/common_language',
 'opener-project/coreference-base',
 'khzaw/athena',
 'cogenda/cgdrep',
 'jonschlinkert/common-words',
 'microsoft/LID-tool',
 'srijan14/Document-Machine-Translation',
 'tonianelope/Multilingual-BERT',
 'RimWorld-zh/RimWorld-English',
 'TotalVerb/EnglishText.jl',
 'p1u3o/MiWifi-Language-Mod',
 'humenda/isolang-rs',
 'gokhansisman/Language-Support',
 'rljacobson/JLCPCBBasicLibrary',
 'edigu/almanca',
 'mauryquijada/word-complexity-predictor',
 'brackendev/ELIZA-Smalltalk',
 'prashishh/Devanagari-Unicode',
 'fibanneacci/langplusplus',
 'azu/nlp-pattern-match',
 'tedunderwood/noveltmmeta',
 'JEnglishOrg/JEnglish',
 'akio-tomiya/intro_julia_minimum',
 'djstrong/PL-Wiktionary-To-Dictionary',
 'hagronnestad/tjc-usart-hmi-english-patch',
 'Prior99/node-espeak',
 'Helloisa22/Naruto-CardHouver',
 'swirldev/translations',
 'Toluwase/Word-Level-Language-Identification-for-Resource-Scarce-',
 'anushkrishnav/ALANG',
 'gasolin/lingascript',
 'Kaljurand/Grammars',
 'nanaian/english',
 'zhaoweih/countries_json',
 'vk4arm/pysoundex',
 'comdet/SnapOCR',
 'karakorakura/Sign-Language-Interpreter',
 'henryfriedlander/Crossword-Puzzle-Maker',
 'A9T9/Baidu-OCR-API',
 'klumsy/DayBreak-ChinesePowerShell',
 'dialogflow/fulfillment-multi-locale-nodejs',
 'rempelj/rawchars',
 'denman2328/Help',
 'qixuanHou/Mapping-My-Break',
 'cetinsamet/pos-tagging',
 'hosford42/pyramids',
 'ajbkr/Hence',
 'Kycb42148/MagicMod',
 'TeamLS/Buzz',
 'tshrinivasan/dhvani-tts',
 'codingXiaxw/CustomerManagement',
 'DanWahlin/CustomerManager',
 'DanWahlin/CustomerManagerStandard',
 'Tophold/FinancialCustomerView',
 'spring-cloud-samples/customers-stores',
 'microsoft/Windows-appsample-customers-orders-database',
 'eventuate-examples/eventuate-examples-java-customers-and-orders',
 'Featuretools/predict-customer-churn',
 'eventuate-tram/eventuate-tram-examples-customers-and-orders',
 'eventuate-tram/eventuate-tram-sagas-examples-customers-and-orders',
 'CarryChang/Customer_Satisfaction_Analysis',
 'Yoctol/react-messenger-customer-chat',
 'WenRichard/Customer-Chatbot',
 'DanWahlin/Angular-NodeJS-MongoDB-CustomersService',
 'MicrosoftDocs/dynamics-365-customer-engagement',
 'KazukiOnodera/Santander-Customer-Transaction-Prediction',
 'chatopera/chatbot.catalog.customer-service',
 'ewangke/CustomersAlsoReviewed-AppStore',
 'Vinai/customer-activation',
 'xamarin/customer-success-samples',
 'magefan/module-login-as-customer',
 'rstudio/keras-customer-churn',
 'Acrotrend/Awesome-Customer-Analytics',
 'aws-samples/amazon-lex-customerservice-workshop',
 'bradtraversy/customerbase',
 'searobbersduck/CustomerServiceAI',
 'bradtraversy/restify_customer_api',
 'maifeng/customer-review-crawler',
 'jalajthanaki/Customer_segmentation',
 'DanWahlin/Angular-ASPNET-Core-CustomersService',
 'pimcore/customer-data-framework',
 'edavis10/redmine-customer-plugin',
 'magepal/magento2-guest-to-customer',
 '6ag/customer-service',
 'WLOGSolutions/telco-customer-churn-in-r-and-h2o',
 'IBM/customer-loyalty-program',
 'IBM/customer-loyalty-program-hyperledger-fabric-VSCode',
 'customerio/customerio-ruby',
 'chargebee/customer-portal-php',
 'moov-io/customers',
 'Azure-Samples/functions-customer-reviews',
 'integer-net/RemoveCustomerAccountLinks',
 'Asutosh11/CustomerSupportChat',
 'DanWahlin/AngularCLI-ASPNET-Core-CustomersService',
 'feistiller/weixinCustomerService',
 'm2-systemcode/BrazilCustomerAttributes',
 'Azure-Samples/customer-car-reviews',
 'skrusche63/customerml',
 'VanHakobyan/CustomerRelationshipManagement_CRM',
 'deved-it/magento2-disable-customer-registration',
 'treselle-systems/customer_churn_analysis',
 'customerio/customerio-python',
 'bradtraversy/customer-cli',
 'erictam96/E-commerceCustomerFYP',
 'yemiwebby/nest-customer-list-app',
 'magepal/magento2-customer-account-links-manager',
 'camunda-consulting/showroom-customer-onboarding',
 'eventuate-tram/eventuate-tram-examples-customers-and-orders-redis',
 'xiaogp/customer_churn_prediction',
 'nahidalam/customer_bot',
 'annalucia1/Customer-Behavior-Analysis-Recommendation',
 'UserScape/php-customerio',
 'enrico69/magento2-customer-activation',
 'tnmichael309/Kaggle-Santander-Customer-Transaction-Prediction-5th-Place-Partial-Solution',
 'dmnWebDesign/vue-fb-customer-chat',
 'MicrosoftLearning/MB-200-Dynamics365CustomerEngagementCore-',
 'ajzele/Inchoo_LoginAsCustomer',
 'ldulcic/customer-support-chatbot',
 'rzayevsahil/Customer-Management-System-for-Coffee-Shops',
 'DanWahlin/AngularCLI-NodeJS-MongoDB-CustomersService',
 'IBM/telco-customer-churn-on-icp4d',
 'marvinlabs/customer-area',
 'rafaelpatro/google-customer-reviews',
 'MaartenGr/CustomerSegmentation',
 'jalajthanaki/Customer_lifetime_value_analysis',
 'alosdev/CustomersChoice',
 'IBM/customer-churn-prediction',
 'eventuate-tram-examples/eventuate-tram-examples-micronaut-customers-and-orders',
 'looker/customer-scripts',
 'li-keli/customerService_Core',
 'mceliksoy/CustomerDemo',
 'wshuyi/demo-customer-churn-ann',
 'weifuchuan/customer-service',
 'firegento/firegento-customer',
 'naomifridman/Deep-VAE-prediction-of-churn-customer',
 'Vinai/module-customer-password-command',
 'devmentors/DNC-DShop.Services.Customers',
 'facebookincubator/wordpress-messenger-customer-chat-plugin',
 'fateh491989/customersupport',
 'zy445566/CustomerService',
 'LIANSAI/Customers-purchase-Prediction',
 'kpei/Customer-Analytics',
 'lsvih/chinese-customer-review',
 'Sylius/CustomerOrderCancellationPlugin',
 'gmasse/ovh-ipxe-customer-script',
 'watson-developer-cloud/social-customer-care',
 'Azure/cortana-intelligence-customer360',
 'ELMAHDI-AR/CustomerAuthentication-With-ASP.NET-MVC',
 'Sylius/CustomerReorderPlugin',
 'rileypredum/mall_customer_segmentation'

    
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