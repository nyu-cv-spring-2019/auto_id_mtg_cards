# auto_id_mtg_cards
This software will automatically identify magic the gathering playing cards after taking a photo of them.

## Setup:
1) clone repo:
```
git clone https://github.com/nyu-cv-spring-2019/auto_id_mtg_cards.git
```
2) go into repo:
```
cd auto_id_mtg_cards
```
3) install all the dependencies:
```
python -m pip install -r requirements.txt
```

## Usage:
There are 3 commands you can run. See help if you need more info:
```
python auto_mtg_cli.py --help
```
#### Commands:
This command will find the set for an image you provide:
```
python auto_mtg_cli.py run-set-compare [IMAGE_PATH]
```
It has some options you can give it. One intresting option being --use-cv2-cross-corr. 
This will use cv2 internal cross-corr instead of our implementation. Our implementation 
works fine.

This command will find the card that is in your image and give you back the name and
the price you can sell it for on the market(tcgplayer.com)"
```
python auto_mtg_cli.py run-card-compare [IMAGE_PATH]
```
It has some options you can give it. One intresting option being --use-cv2-cross-corr. 
This will use cv2 internal cross-corr instead of our implementation. Our implementation 
does not work well so whenever you can use:
```
python auto_mtg_cli.py run-card-compare [IMAGE_PATH] --use-cv2-cross-corr True
```

This command gives a confusion matrix:
```
python auto_mtg_cli.py run-confusion-matrix
```

## Provided test images:
For convenience we provided some test images so to run a set compare:
```
python auto_mtg_cli.py run-set-compare mtg_test_photos/mtg_rna.jpg
```

## Contributing:
Fork repo and make a pull request!
