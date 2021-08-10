import cv2
import numpy as np



def reshape_outer_contour(points , img):
    done = False
    current = (0, 0)
    prev_current = (0,0)
    
    #Edit mode parameters
    EDIT_MODE = False
    edit_idx  = 0;
    radius = 3
    
    clone = img.copy()
    #adding dots to the polygons
    for coords in points:
        x,y = coords
        cv2.circle(img,(x,y),radius,(0,200,0),-1)

    #Used inside the while loop

    temp = img.copy()

    params = [points, clone, temp, done, current, prev_current, EDIT_MODE, edit_idx, radius]
    

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_mouse, params)
    
    

    while(not done): 
        #update variables
        points = params[0]
        clone = params[1]
        temp  = params[2]
        done = params[3]
        current = params[4]
        prev_current = params[5]
        EDIT_MODE = params[6]
        edit_idx = params[7]
 
     

        # This is our drawing loop, we just continuously draw new images
        # and show them in the named window
        if (len(points) > 1):
            if(current != prev_current):
                img = temp.copy()


            # Draw all the current polygon segments
            cv2.polylines(img, [np.array(points)], False, (255,0,0), 1)

            cv2.line(img, (points[0][0],points[0][1]), (points[len(points)-1][0],points[len(points)-1][1]), (255,0,0)) #edge case

            #When Edit Mode is activated adjust segments
            if EDIT_MODE:
                # And  also show what the current segment would look like
                cv2.line(img, (points[edit_idx-1][0],points[edit_idx-1][1]), current, (0,0,255)) 
                cv2.circle(img,current,radius,(0,200,0),-1) #TARGET

                if edit_idx+1 == len(points): #bug fix when reaching end of array
                    cv2.line(img, (points[0][0],points[0][1]), current, (0,0,255))
                else:
                    cv2.line(img, (points[edit_idx+1][0],points[edit_idx+1][1]), current, (0,0,255))



        # Update the window
        cv2.imshow("image", img)
        # And wait 50ms before next iteration (this will pump window messages meanwhile)

        if cv2.waitKey(50) == ord('d'): # press d(done)
            done = True

    # User finised entering the polygon points, so let's make the final drawing
    cv2.destroyWindow("image")
    return points


    img = clone.copy()
    # of a filled polygon
    if (len(points) > 0):
        cv2.fillPoly(img, np.array([points]), (255,0,0))
    # And show it
    cv2.imshow("image", img)
    # Waiting for the user to press any key
    cv2.waitKey(0)
    cv2.destroyWindow("image")
    
    

    
    
def on_mouse(event, x, y, buttons, params):
        points = params[0]
        clone = params[1]
        temp  = params[2]
        done = params[3]
        current = params[4]
        prev_current = params[5]
        EDIT_MODE = params[6]
        edit_idx = params[7]
        radius = params[8]
 
        # Mouse callback that gets called for every mouse event (i.e. moving, clicking, etc.)
        if done: # Nothing more to do
            return
        if event == cv2.EVENT_MOUSEMOVE:
            # We want to be able to draw the line-in-progress, so update current mouse position
            current = (x, y)
          
        elif event == cv2.EVENT_LBUTTONDOWN:
            # Left click means adding a point at current position to the list of points
            
            if not EDIT_MODE:
                L2_eq = np.array(points) - np.array([[x,y]])
                DISTANCE_MOUSE_TO_DOTS = np.linalg.norm(L2_eq,ord=2,axis=1,keepdims=True) 
                INDEX_NEAREST_NEIGHBOUR = list(DISTANCE_MOUSE_TO_DOTS).index(np.min(DISTANCE_MOUSE_TO_DOTS))


                #This activates edit mode if distance is short enough when a click is done
                if np.min(DISTANCE_MOUSE_TO_DOTS) < 5:
                    EDIT_MODE = True
                    edit_idx = INDEX_NEAREST_NEIGHBOUR



            if EDIT_MODE:
                points[edit_idx] = [x,y] 

                #other_temp makes sure that dot is added properly when a change happens
                other_temp = clone.copy()
                for coords in points:
                    x,y = coords
                    cv2.circle(other_temp,(x,y),radius,(0,200,0),-1)

                temp = other_temp.copy()

        #Disable Edit mode 
        elif event == cv2.EVENT_LBUTTONDBLCLK:
            print("Adding point #%d with position(%d,%d)" % (edit_idx, x, y))
            EDIT_MODE = False




        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click means we're done
            print("Completing polygon with %d points." % len(points))
            done = True
            
            
        #update params
        params[0] = points
        params[1] = clone
        params[2] = temp
        params[3] = done
        params[4] = current
        params[5] = prev_current
        params[6] = EDIT_MODE
        params[7] = edit_idx
 