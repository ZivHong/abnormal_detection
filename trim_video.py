import cv2
import concurrent.futures

video_dir = '/mnt/hdd/ucf_crime/Videos/' #ucf_crime path
video_label = ['Abuse','Arrest','Arson','Assault','Burglary','Explosion','Fighting','Normal_Videos_event','RoadAccidents','Robbery','Shooting','Shoplifting','Stealing','Vandalism'] # 14 classes
save_dir = 'ucfcrime_trimmed/'
def read_annotation():
    video_list = []
    with open("ucf_crime_temporal_annotation.txt", mode="r") as txtfile:
        video_list = txtfile.read().splitlines() 
    return video_list

def trim_video(annotation):
    
    # row[] ->  0:videoname , 1:label , 2:start1 , 3:end1 , 4:start2 , 5:end2
    anno_row = annotation.split(' ', 5)
    origin_video = video_dir + video_label[int(anno_row[1])-1] + '/' + anno_row[0]
    output_v1 = save_dir + anno_row[0][0:-4] + '_trimmed_1.mp4'
    title=anno_row[0][0:-9]
    extract_video(origin_video,output_v1,anno_row[2],anno_row[3],title + ' 1')

    if(anno_row[4] != str(-1)):
        output_v2 = save_dir + anno_row[0][0:-4] + '_trimmed_2.mp4'
        extract_video(origin_video,output_v2,anno_row[4],anno_row[5],title + ' 2')
    
def extract_video(origin_video,output_video,start_frame,end_frame,title):
    cap = cv2.VideoCapture(origin_video)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video,fourcc,30.0,(224,224))

    diff = int(end_frame) - int(start_frame)   
    cap.set(1, int(start_frame))

    for i in range(diff):
        ret, frame = cap.read()
        if not ret:
            print(title + ' fail')
            break
        frame = cv2.resize(frame,(224,224))
        out.write(frame)
    out.release()
    cap.release()
    print(title + ' complete')

if __name__ == "__main__":
    anno_list = read_annotation()
    count =0 
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as executor:
        executor.map(trim_video, anno_list)
    # for row  in anno_list:
    #     col = row.split(' ', 5)
    #     count += 1
    #     if (col[4] != str(-1)): 
    #         count +=1
    # print(count)
