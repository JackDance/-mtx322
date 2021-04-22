
def calculate_inter_area(box1, box2):
    '''
    :param box1: Box对象
    :param box2: Box对象
    :return: box1与box2的相交面积
    '''
    left_x, left_y = max([box1.x, box2.x]), max([box1.y, box2.y])
    right_x, right_y = min([box1.x + box1.w, box2.x + box2.w]), \
                       min([box1.y + box1.h, box2.y + box2.h])
    height = right_y - left_y
    width = right_x - left_x
    area = height * width if height > 0 and width > 0 else 0
    return area

class Box:
    # x,y是左上角坐标
    def __init__(self, x, y, w, h, category=None, confidence=None):
        self.category = category
        self.confidence = confidence
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_area(self):
        return self.w * self.h

    def get_iou(self, box2):
        inter_area = calculate_inter_area(self, box2)
        return inter_area / (self.get_area() + box2.get_area() - inter_area)

def get_det_eval(y_true, y_pred, iou_thres=0.1, confidence_thres=0.25):

    '''
    Args:
        y_true:  ground truth值，格式和y_pred完全一致，只是其score不会被用到，可以随便填一个值。
        y_pred:  检测模型产生的结果, 是一个3层的list。第1层是图片级别信息的集合；第2层是bbox级别信息的集合；
        第3层是单个bbox的结果，其格式为[x, y, w, h, score, class_id]。
        示例：[[], [[x, y, w, h, score, class_id], [x, y, w, h, score, class_id]], [], 
                [[x, y, w, h, score, class_id]]]。
        iou_thres:
        confidence_thres:
    returns:
        res: dict of metric results, includes total_gts, total_dts, miss_det, over_det, 
             miss_det_rate, over_det_rate
    '''
    total_gts, total_dts, over_det, miss_det = 0, 0, 0, 0
    res = dict()
    new_y_pred = [[] for _ in y_pred]
    for i, predict_img in enumerate(y_pred):
        for predict_box in predict_img:
            if predict_box[4] >= confidence_thres:
                new_y_pred[i].append(predict_box)
                total_dts += 1
    for img_file in range(len(y_true)):
        total_gts += len(y_true[img_file])
        necessary = False
        temp = []
        for obj in y_true[img_file]:
            x, y, w, h = obj[0], obj[1], obj[2], obj[3]
            gt_box = Box(x, y, w, h, obj[5])
            false_negative = True
            for i, predict_img in enumerate(new_y_pred[img_file]):
                predict_box = Box(predict_img[0], predict_img[1],
                                  predict_img[2], predict_img[3],
                                  predict_img[5], predict_img[4])
                if gt_box.get_iou(predict_box) > iou_thres:
                    false_negative = False
                    temp.append(i)
            if false_negative:
                miss_det += 1
        for i, predict_img in enumerate(new_y_pred[img_file]):
            if i not in temp:
                over_det += 1
    res['total_gts'] = total_gts
    res['total_dts'] = total_dts
    res['miss_det'] = miss_det
    res['over_det'] = over_det
    res['miss_det_rate'] = miss_det / (total_gts if total_gts else 1)
    res['over_det_rate'] = over_det / (total_dts if total_dts else 1)
    return res

if __name__ == '__main__':
    pass

