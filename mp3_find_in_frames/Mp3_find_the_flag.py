import sys
import base64

with open(sys.argv[1],"rb") as mp3file:
    data = mp3file.read()# read the whole file
    
length = len(data) # store the length, just for efficiency
index = 0
result = b''
bitrate_index = [0,32,40,48,56,64,80,96,112,128,160,192,224,256,320,-1]
samplingrate_index = [44.1, 48, 32, 0]
while(1):
 index = data.find(b'\xFF\xFB', index) # search for audio-header
 if index == -1 or index+5 >= length: break # check if NOT found
 bitrate = bitrate_index[data[index+2]>>4] # get bitrate
 samplingrate = samplingrate_index[(data[index+2]&0xc)>>2] #get samplingrate
 padding = (data[index+2]&0x2)>>1 #get padding
 frame_len = int(144 * bitrate / samplingrate) + padding #calculate Frame-length
 index += frame_len # add to the Index (pointer)
 nextIndex = data.find(b'\xFF\xFB', index) # get next position
 if nextIndex != -1:
  diff = nextIndex - index #check for extra-data
  if diff > 0:
   result += data[index:index+diff] #append extra-data
print(result)
print(base64.b64decode(result)) #print Base64-decoded extra-data
