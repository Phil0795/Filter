import base64
import pandas as pd

# Take the OneDrive shared Link and convert it to a direct download link of the file
def create_onedrive_directdownload (onedrive_link):
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    return resultUrl

onedrive_link = "https://1drv.ms/x/s!Aplkl7YI-6KNm0SwdxIMtJcKZlmK?e=0X33NY"
onedrive_dd = create_onedrive_directdownload(onedrive_link)
print(onedrive_link)
print(onedrive_dd)
df = pd.read_excel(onedrive_dd)
df.head()