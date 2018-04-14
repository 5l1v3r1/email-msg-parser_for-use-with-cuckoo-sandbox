# Cuckoo Sandbox utility script for analyzing email attachments

Cuckoo Sandbox utility script for analyzing email attachments inside .msg files (Microsoft Outlook files) and exporting their analysis results to a Microsoft Excel file (.xlsx file).  This is mainly for Malware Analysts that want to stay organized when analyzing multiple email messages.

## Getting Started

Run python script (.py file) after modifying the hard-corded Cuckoo Sandbox URLs and file paths to .msg files.

### Prerequisites

* Cuckoo Sandbox instance
* Python 2.7 with following non-standard packages:
    * olefile==0.43
        * sudo pip install olefile==0.43
    * xlwt (Microsoft Excel file package)
        * sudo pip install xlwt

## Built With

* Eclipse Oxygen with PyDev Eclipse plugin

## Authors

* **Mark Conover** - [GitHub](https://github.com/markconover)

See also the list of [contributors](https://github.com/markconover/email-msg-parser_for-use-with-cuckoo-sandbox/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* **Matthew Walker** - *The code for parsing .msg files was copied/revised from this author" - https://github.com/mattgwwalker/msg-extractor
