import time
import torch
from craft_text_detector import  get_prediction,export_detected_regions, export_extra_results
import numpy as np
def get_Boxes(image,output_dir= 'outputs/'):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    start_time=time.time()
    craft_net = torch.load('OCR/detect_model/craft.pt').to(device)
    refine_net = torch.load('OCR/detect_model/refine_net.pt').to(device)
    prediction_result = get_prediction(
        image=image,
        craft_net=craft_net,
        refine_net=refine_net,
        text_threshold=0.7,
        link_threshold=0.2,
        low_text=0.5,
        cuda=True,
        long_size=1280
    )
    # exported_file_paths = export_detected_regions(
    #     image=image,
    #     regions=prediction_result["boxes"],
    #     output_dir=output_dir,
    #     rectify=True
    # )
    # export_extra_results(
    #     image=image,
    #     regions=prediction_result["boxes"],
    #     heatmaps=prediction_result["heatmaps"],
    #     output_dir=output_dir
    # )
    end_time=time.time()
    print('文字偵測花費: ',end_time-start_time,'秒')
    boxes = (prediction_result['boxes'])
    result = []
    data = []
    for i in boxes:
        result.append([int(i[0][0]), int(i[0][1]), int(i[2][0]), int(i[2][1])])
        data.append(int(i[0][0]))
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outlier = [i for i in range(len(data)) if data[i] > upper_bound or data[i] < lower_bound]
    return result,outlier
