import csv
import datetime
import json
import os
import shutil


def check_metrics_json(out_dir):
    file_name = os.path.join(out_dir, 'metrics.json')
    if os.path.exists(file_name):
        os.remove(file_name)
    # current = datetime.datetime.strftime(datetime.datetime.now(),
    #  '%Y-%m-%d %H:%M:%S')
    # dic = {"run_data_time": current}
    # with open(file_name, 'w') as r:
    #     json.dump(dic, r)


# 写入时间或数据
def write_csv(res, out_dir):
    dirs = out_dir.split('/')
    out_csv = os.path.join(dirs[0], dirs[1], 'best_record.csv')
    with open(out_csv, "a", encoding='utf-8', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(res) # res为写入的时间或数据

#
def analyze_seg_metrics(json_file, out_dir='./', model_id=-1, start=0):
    current = datetime.datetime.strftime(datetime.datetime.now(),
                                         '%Y-%m-%d %H:%M:%S') # 获取当前时间
    write_csv([current, out_dir, model_id], out_dir)

    best_bbox_ap50 = 0
    with_segm_ap50 = 0

    best_segm_ap50 = 0
    with_bbox_ap50 = 0

    best_aver_ap50 = 0
    with_aver_bbox_ap50 = 0
    with_aver_segm_ap50 = 0

    best_miss_det_rate = float('inf') # 初始化为无穷大
    with_over_det_rate = float('inf')

    best_over_det_rate = float('inf')
    with_miss_det_rate = float('inf')

    best_bbox_iteration = -1
    best_segm_iteration = -1
    best_aver_iteration = -1
    best_miss_det_rate_iteration = -1
    best_over_det_rate_iteration = -1

    miss_over = False # 控制

    with open(json_file, 'rb') as f:
        for line in f.readlines():
            json_data = json.loads(line) # 将已编码的json字符串解码为python对象
            if 'bbox/AP' in json_data:
                # print(json_data["iteration"])
                if json_data["bbox/AP50"] > best_bbox_ap50:
                    best_bbox_ap50 = json_data["bbox/AP50"]
                    with_segm_ap50 = json_data["segm/AP50"]
                    best_bbox_iteration = json_data["iteration"]

                if json_data["segm/AP50"] > best_segm_ap50:
                    best_segm_ap50 = json_data["segm/AP50"]
                    with_bbox_ap50 = json_data["bbox/AP50"]
                    best_segm_iteration = json_data["iteration"]

                aver_bbox_segm_ap50 = (json_data["segm/AP50"] +
                                       json_data["bbox/AP50"]) / 2
                if aver_bbox_segm_ap50 > best_aver_ap50:
                    best_aver_ap50 = aver_bbox_segm_ap50
                    with_aver_bbox_ap50 = json_data["bbox/AP50"]
                    with_aver_segm_ap50 = json_data["segm/AP50"]
                    best_aver_iteration = json_data["iteration"]

                if "det_eval/miss_det" in json_data and json_data["iteration"] >= start:
                    miss_over = True
                    if json_data["det_eval/miss_det_rate"] < best_miss_det_rate:
                        best_miss_det_rate = json_data["det_eval/miss_det_rate"]
                        with_over_det_rate = json_data["det_eval/over_det_rate"]
                        best_miss_det_rate_iteration = json_data["iteration"]

                    if json_data["det_eval/over_det_rate"] < best_over_det_rate:
                        best_over_det_rate = json_data["det_eval/over_det_rate"]
                        with_miss_det_rate = json_data["det_eval/miss_det_rate"]
                        best_over_det_rate_iteration = json_data["iteration"]

    print('-' * 32 + 'Best bbox AP50' + '-' * 32)
    print("Best bbox AP50: \033[1;31m{:.2f}\033[0m, "
          "iteration: \033[1;32m{}\033[0m, "
          "Segm AP50: \033[1;32m{:.2f}\033[0m, "
          "Aver AP50: \033[1;32m{:.2f}\033[0m.".format(
        best_bbox_ap50, best_bbox_iteration, with_segm_ap50,
        (best_bbox_ap50 + with_segm_ap50) / 2))

    write_csv([
        'Best bbox AP50', best_bbox_ap50, 'iteration', best_bbox_iteration,
        'Segm AP50', with_segm_ap50, 'Aver AP50',
        (best_bbox_ap50 + with_segm_ap50) / 2
    ], out_dir)

    print('-' * 32 + 'Best segm AP50' + '-' * 32)
    print("Best segm AP50: \033[1;31m{:.2f}\033[0m, "
          "iteration: \033[1;32m{}\033[0m, "
          "Bbox AP50: \033[1;32m{:.2f}\033[0m, "
          "Aver AP50: \033[1;32m{:.2f}\033[0m.".format(
              best_segm_ap50, best_segm_iteration, with_bbox_ap50,
              (best_segm_ap50 + with_bbox_ap50) / 2))

    write_csv([
        'Best segm AP50', best_segm_ap50, 'iteration', best_segm_iteration,
        'Bbox AP50', with_bbox_ap50, 'Aver AP50',
        (best_segm_ap50 + with_bbox_ap50) / 2
    ], out_dir)

    print('-' * 32 + 'Best aver AP50' + '-' * 32)
    print("Best aver AP50: \033[1;31m{:.2f}\033[0m, "
          "iteration: \033[1;32m{}\033[0m, "
          "Bbox AP50: \033[1;32m{:.2f}\033[0m, "
          "Segm AP50: \033[1;32m{:.2f}\033[0m.".format(best_aver_ap50,
                                                       best_aver_iteration,
                                                       with_aver_bbox_ap50,
                                                       with_aver_segm_ap50))


    write_csv([
        'Best aver AP50', best_aver_ap50, 'iteration', best_aver_iteration,
        'Bbox AP50', with_aver_bbox_ap50, 'Segm AP50', with_aver_segm_ap50
    ], out_dir)

    if miss_over:
        print('-' * 32 + 'Best miss_det rate' + '-' * 28)
        print("Best miss_det rate: \033[1;31m{:.2f}\033[0m, "
              "iteration: \033[1;32m{}\033[0m, "
              "Over_det rate: \033[1;32m{:.2f}\033[0m.".format(
            best_miss_det_rate, best_miss_det_rate_iteration, with_over_det_rate))

        write_csv(['Best miss_det rate', best_miss_det_rate,
                   'iteration', best_miss_det_rate_iteration,
                   'Over_det rate', with_over_det_rate], out_dir)

        print('-' * 32 + 'Best over_det rate' + '-' * 28)
        print("Best over_det rate: \033[1;31m{:.2f}\033[0m, "
              "iteration: \033[1;32m{}\033[0m, "
              "Miss_det rate: \033[1;32m{:.2f}\033[0m.".format(
            best_over_det_rate, best_over_det_rate_iteration, with_miss_det_rate))

        write_csv(['Best miss_det rate', best_miss_det_rate,
                   'iteration', best_miss_det_rate_iteration,
                   'Over_det rate', with_over_det_rate], out_dir)

    print('-' * 78)


    out_dir, _ = os.path.split(json_file) # ('C:\\Users\\Jack\\Desktop\\mtx322', 'eval_res.json')
    with open(json_file, 'rb') as f:
        for line in f.readlines():
            json_data = json.loads(line)
            if 'bbox/AP' in json_data:
                model_name = 'model_' + str(
                    json_data["iteration"]).zfill(7) + '.pth'
                model_name = os.path.join(out_dir, model_name)

                if os.path.exists(model_name):
                    if json_data["iteration"] == best_bbox_iteration:
                        out_model = os.path.join(out_dir,
                                                 'model_best_bbox.pth')
                        if os.path.exists(out_model):
                            os.remove(out_model)
                        shutil.copy(model_name, out_model)

                    if json_data["iteration"] == best_segm_iteration:
                        out_model = os.path.join(out_dir,
                                                 'model_best_segm.pth')
                        if os.path.exists(out_model):
                            os.remove(out_model)
                        shutil.copy(model_name, out_model)

                    if json_data["iteration"] == best_aver_iteration:
                        out_model = os.path.join(out_dir, 'model_best.pth')
                        if os.path.exists(out_model):
                            os.remove(out_model)
                        shutil.copy(model_name, out_model)

                    if miss_over:
                        if json_data["iteration"] == best_miss_det_rate_iteration:
                            out_model = os.path.join(out_dir, 'model_best_miss.pth')
                            if os.path.exists(out_model):
                                os.remove(out_model)
                            shutil.copy(model_name, out_model)

                        if json_data["iteration"] == best_over_det_rate_iteration:
                            out_model = os.path.join(out_dir, 'model_best_over.pth')
                            if os.path.exists(out_model):
                                os.remove(out_model)
                            shutil.copy(model_name, out_model)
                    os.remove(model_name)


    check_point = os.path.join(out_dir, 'last_checkpoint')
    if os.path.exists(check_point):
        os.remove(check_point)
    with open(check_point, 'w', encoding='utf-8', newline="") as f:
        f.write('model_best.pth')


# 这个还没增加漏检和过杀
def analyze_obj_metrics(json_file, out_dir='./', model_id=-1):
    current = datetime.datetime.strftime(datetime.datetime.now(),
                                         '%Y-%m-%d %H:%M:%S')
    write_csv([current, out_dir, model_id], out_dir)

    best_bbox_ap50 = 0
    best_bbox_iteration = -1

    with open(json_file, 'rb') as f:
        for line in f.readlines():
            json_data = json.loads(line)
            if 'bbox/AP' in json_data:
                # print(json_data["iteration"])
                if json_data["bbox/AP50"] > best_bbox_ap50:
                    best_bbox_ap50 = json_data["bbox/AP50"]
                    best_bbox_iteration = json_data["iteration"]


    print('-' * 13 + 'Best bbox AP50' + '-' * 13)
    print("Best bbox AP50: \033[1;31m{:.2f}\033[0m, "
          "iteration: \033[1;32m{}\033[0m.".format(best_bbox_ap50,
                                                   best_bbox_iteration))
    print('-' * 40)


    write_csv(
        ['Best bbox AP50', best_bbox_ap50, 'iteration', best_bbox_iteration],
        out_dir)

    out_dir, _ = os.path.split(json_file)
    with open(json_file, 'rb') as f:
        for line in f.readlines():
            json_data = json.loads(line)
            if 'bbox/AP' in json_data:
                model_name = 'model_' + str(
                    json_data["iteration"]).zfill(7) + '.pth'
                model_name = os.path.join(out_dir, model_name)

                if os.path.exists(model_name):
                    if json_data["iteration"] == best_bbox_iteration:
                        out_model = os.path.join(out_dir, 'model_best.pth')
                        if os.path.exists(out_model):
                            os.remove(out_model)
                        shutil.copy(model_name, out_model)
                    os.remove(model_name)

    check_point = os.path.join(out_dir, 'last_checkpoint')
    if os.path.exists(check_point):
        os.remove(check_point)
    with open(check_point, 'w', encoding='utf-8', newline="") as f:
        f.write('model_best.pth')


if __name__ == "__main__":
    json_file = 'eval_res.json'
    analyze_obj_metrics(json_file)
