# QD-IMD: Quick Draw Irregular Mask Dataset
![Masked CelebA](https://raw.githubusercontent.com/karfly/qd-imd/master/readme/celeba_masked_6_examples.png)

[Inpainting](https://en.wikipedia.org/wiki/Inpainting) is an important computer vision task, where goal is to restore masked parts of an image. E.g., inpainting can help in erasing from photo something unwanted like passing bystander or your ex-partner.

Many recent approaches focus on rectangular shaped holes, often assumed to be center in the image. These limitations are absolutely not practical, because we often need to erase something with irregular form. That's why we need dataset with masks of irregular forms.

Guilin Liu *et al.* in their [recent paper](https://arxiv.org/abs/1804.07723) proposed such dataset, where source of irregular patterns were the results of occlusion/dis-occlusion mask estimation method between two consecutive frames for videos. Paper showed good results in inpainting, but we think their dataset has some weaknesses:
- There is nothing "human" in generating such masks
- Masks often have sharp edges because of rough crops close to borders
- It's not public (though authors claimed, they were going to release it)

##### NVidia Irregular Mask Dataset [[1]](https://arxiv.org/abs/1804.07723):
![NVidia Irregular Mask Dataset examples](https://raw.githubusercontent.com/karfly/qd-imd/master/readme/nvidia_imd_6_examples.png)

##### Our Irregular Mask Dataset (QD-IMD):
![Quick Draw Irregular Mask Dataset examples](https://raw.githubusercontent.com/karfly/qd-imd/master/readme/qd_imd_6_examples.png)

We decided to fight these problems and generated **QD-IMD** (Quick Draw Irregular Mask Dataset).

## How it's generated
Our dataset is based on Quick Draw dataset (a collection of 50 million human drawings). Our hypothesis is that combination of strokes drawn by human hand is a good source of patterns for irregular masks. Here are steps for generating a single mask (default values are given in square brackets):
1. Randomly choose number of strokes for mask [*~N(4, 2)*]
2. Randomly sample strokes from Quick Draw dataset
3. For each stroke choose width (px) [*~Uniform(5, 15)*] and draw it on canvas
4. Sample upscale rate [*~Uniform(1.0, 1.5)*] and upscale canvas correspondingly
5. Make central crop of target shape [*(512, 512)*]
6. Binarize resulting mask

*Note: all parameters can changed for a specific task*

## Download dataset
Dataset can be downloaded from [Dropbox](https://www.dropbox.com/s/ui4zgw7dhe9v1ju/qd_imd.tar.gz?dl=0) of [Yandex.Disk](https://yadi.sk/d/6A5M-5ge3YKqXK).


## Reproduce dataset
First clone this repository:
```bash
git clone https://github.com/karfly/qd-imd
cd qd-imd
```

Then download Quick Draw (simplified). It's located on Google Cloud [here](https://console.cloud.google.com/storage/browser/quickdraw_dataset/full/simplified). You can install `gsutil` following [these instructions](https://cloud.google.com/storage/docs/gsutil_install) and execute command:
```bash
mkdir quickdraw_simplified
gsutil -m cp -R gs://quickdraw_dataset/full/simplified/ quickdraw_simplified
```

**(!)** *Note: Quick Draw (simplified) weight is **~22Gb**. If it's not suitable for you, just download part of the dataset, and everything will work correctly*
 
To reproduce dataset or generate masks with other parameters you'll need Python 3 with install packages specified in `requirements.txt`. You can use pip:
```bash
pip install -r requirements.txt
```

Then run:
```bash
python generate_dataset.py
```

To get detailed information about parameters execute:
```bash
python generate_dataset.py --help
```

## Future work
- Create vector version of the dataset

## References
- [1] [Image Inpainting for Irregular Holes Using Partial Convolutions](https://arxiv.org/abs/1804.07723)
- [2] [CelebA dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)


