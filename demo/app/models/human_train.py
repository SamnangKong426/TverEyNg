from ultralytics import YOLO, checks, hub
checks()

hub.login('3c22078e18ed4bd513954eb096328f8465aca49109')

model = YOLO('https://hub.ultralytics.com/models/ZhkbUazas23PkONYk5Ls')
results = model.train()