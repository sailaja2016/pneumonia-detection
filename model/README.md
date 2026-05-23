# model/README.md

## How to add your trained CNN model

Place your trained Keras model file here as:

    model/pneumonia_model.h5

---

## Training the model (optional — for the real CNN)

If you want to train your own model from the Kaggle chest X-ray dataset:

1. Download the dataset from:
   https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia

2. Unzip it. You'll get a folder structure like:
   chest_xray/
     train/
       NORMAL/
       PNEUMONIA/
     val/
       NORMAL/
       PNEUMONIA/
     test/
       NORMAL/
       PNEUMONIA/

3. Run the training script:
   python train_model.py

   This will produce: model/pneumonia_model.h5

4. Restart the Flask app — it will automatically load the real model.

---

## Without a model (Demo Mode)

If no model file is found, the app runs in **Demo Mode**
where predictions are randomly generated.
This is still useful to show the full UI and workflow.
