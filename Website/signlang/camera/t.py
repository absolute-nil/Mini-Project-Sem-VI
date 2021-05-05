def getUsers(request,Product_id):   
    queryset=Auction.objects.filter(ProductID=Product_id).order_by('-ClientInitialBid')
    return JsonResponse({'users':list(queryset.values())})


global a
b=True
def facecam_feed(request,p_id):
    try:
        global a
        a=Hand_gesture(p_id,request.user.username)
        return StreamingHttpResponse(gen(a), content_type="multipart/x-mixed-replace;boundary=frame")
    except: 
        pass

$(#display).append(response);
    $('#display').empty();


def gen(camera):
    global b
    b=True
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class Hand_gesture():
    def __init__(self,p_id,uname):
        self.vs = VideoStream(src=0).start()
        self.fps = FPS().start()
        self.p_id= p_id
        self.uname=uname

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        # grab the frame from the threaded video stream
        img = self.vs.read()
        img = cv2.flip(img, 1)

        cv2.rectangle(img, (250, 200), (25, 25), (0, 255, 0), 0)
        crop_img = img[25:200, 25:250]

        # convert to grayscale
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # applying gaussian blur
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)

        # thresholdin: Otsu's Binarization method
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # show thresholded image


        # check OpenCV version to avoid unpacking error
        (version, _, _) = cv2.__version__.split('.')

        if version == '3':
            image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
                                                          cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        elif version == '4':
            contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, \
                                                   cv2.CHAIN_APPROX_NONE)

        # find contour with max area
        cnt = max(contours, key=lambda x: cv2.contourArea(x))

        # create bounding rectangle around the contour (can skip below two lines)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)

        # finding convex hull
        hull = cv2.convexHull(cnt)

        # drawing contours
        drawing = np.zeros(crop_img.shape, np.uint8)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)

        # finding convex hull
        hull = cv2.convexHull(cnt, returnPoints=False)

        # finding convexity defects
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0
        cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

        # applying Cosine Rule to find angle for all defects (between fingers)
        # with angle > 90 degrees and ignore defects
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]

            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

            # apply cosine rule here
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

            # ignore angles > 90 and highlight rest with red dots
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
            dist = cv2.pointPolygonTest(cnt, far, True)

            # draw a line from start to end i.e. the convex points (finger tips)
            # (can skip this part)
            cv2.line(crop_img, start, end, [0, 255, 0], 2)
            cv2.circle(crop_img, far, 5, [0, 0, 255], -1)
            
        maxbid=Auction.objects.filter(ProductID=self.p_id).aggregate(Max('ClientInitialBid'))["ClientInitialBid__max"]
        userbid=Auction.objects.get(ProductID=self.p_id,ClientUsername=self.uname)
        
        global count
        # define actions required
        if count_defects == 1:
            cv2.putText(img, "2 Fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            count=2
        elif count_defects == 2:
            cv2.putText(img, "3 Fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            count=3
        elif count_defects == 3:
            cv2.putText(img, "4 Fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            count=4
        elif count_defects == 4:
            cv2.putText(img, "5 Fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            count=5
        else:
            cv2.putText(img, "0 Fingers", (50, 50), \
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            if count!=0:
                userbid.ClientInitialBid=math.ceil(maxbid+(maxbid*5*count)/100)
                userbid.save() 
                print(userbid.ClientInitialBid)
                count=0
               

        # show appropriate images in windows

        self.fps.update()
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
