import requests
from bs4 import BeautifulSoup
from load_django import *  
from parser_app.models import Article

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "https://www.reuters.com/sustainability/shareholder-activism/",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Cookie" : '_ga_WBSR7WLTGD=GS2.1.s1759840130$o1$g1$t1759840489$j23$l0$h0; cleared-onetrust-cookies=Thu, 17 Feb 2022 19:17:07 GMT; usprivacy=1---; _li_dcdm_c=.reuters.com; _lc2_fpi=f511229f0ef8--01k6z8f86a8txae2hs6pkt4dcc; _lc2_fpi_js=f511229f0ef8--01k6z8f86a8txae2hs6pkt4dcc; sa-user-id=s%253A0-af0600dd-0de3-5b9c-4b1f-ebafe786ff68.6DN60KFCBNbm2uOpT5NfCv9dGp8MlKfbmcHMQq2mgJc; sa-user-id-v2=s%253ArwYA3Q3jW5xLH-uv54b_aB-A9KA.UkG%252BXWT9aDTCuGfgknl%252BeAu53gPW3ucBiYcpGpBVDt4; sa-user-id-v3=s%253AAQAKIEWZ0dL3xbzDcaxCT-ijmDnzRLWI7zO5c_lkcpmjnlJVEAEYAyCe-LjDBjABOgSVWdHjQgRbYyoq.Ack5Pzce%252BHCQEA2nP1KNcnZFqHMNS3VUsXbPqhPXC9w; _cc_id=ccc6e48eec65c2ac0ed78c3bb6469aaa; panoramaId_expiry=1760442983252; panoramaId=1787f7fde8c7e386ad192ddc950916d53938c268f4cc24bb51a9e964ff5d4a12; panoramaIdType=panoIndiv; _gcl_au=1.1.1481710618.1759838184; permutive-id=2e3019c8-7f6b-4c38-8aa0-7063753732b9; idw-fe-id=bd54a33f-d10e-48e3-9b7c-9b5a0a2f15b9; _fbp=fb.1.1759838184925.487231193620956940; BOOMR_CONSENT="opted-in"; _cb=CxXhk_D4RutECSAHR2; ajs_anonymous_id=c39c2f45-24b8-4d2b-a412-00d59d71dff8; _ga=GA1.2.655027203.1759838188; _gid=GA1.2.1411374942.1759838188; OneTrustWPCCPAGoogleOptOut=false; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+07+2025+15%3A28%3A39+GMT%2B0300+(%D0%B7%D0%B0+%D1%81%D1%85%D1%96%D0%B4%D0%BD%D0%BE%D1%94%D0%B2%D1%80%D0%BE%D0%BF%D0%B5%D0%B9%D1%81%D1%8C%D0%BA%D0%B8%D0%BC+%D0%BB%D1%96%D1%82%D0%BD%D1%96%D0%BC+%D1%87%D0%B0%D1%81%D0%BE%D0%BC)&version=202508.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=231ab4ac-11e0-4a50-9320-74b26d3913e9&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false; ABTasty=uid=kabyqt1551xpw52c&fst=1759838183520&pst=-1&cst=1759838183520&ns=1&pvt=7&pvis=7&th=1428932.0.2.2.1.1.1759840109502.1759840119441.0.1_1428933.1775784.2.2.1.1.1759840109505.1759840119437.0.1_1448016.1800455.2.2.1.1.1759840108793.1759840119425.0.1_1457660.0.2.2.1.1.1759840109509.1759840119443.0.1_1472688.1832381.2.2.1.1.1759840109511.1759840119445.0.1; _li_ss=CpwBCgYI-QEQ9BsKBgj3ARD0GwoFCAoQ9BsKBgjdARD0GwoGCIkBEPQbCgYIgQEQ9BsKBQgMEP4bCgYI9QEQ9BsKBgiHAhD0GwoFCAsQ9BsKBgjjARD0GwoGCKQBEPQbCgYIswEQ9BsKBgiAAhD2GwoGCOEBEPQbCgYIogEQ9BsKBgj_ARD0GwoGCNIBEPQbCgUIfhD0GwoGCIgBEPQbEogBDV9oNQESgAEKBgjKARD0GwoGCOQBEPQbCgYIkwEQ8hsKBgjJARD0GwoGCKUBEPQbCgYI9AEQ8hsKBgiUARDyGwoGCOYBEPQbCgYIxgEQ8xsKBgjHARDyGwoGCOcBEPQbCgYIyAEQ9BsKBgjlARD0GwoGCMUBEPQbCgYI_gEQ9BsKBgjoARD0GxI3DbU-UgsSMAoGCMoBEPQbCgYIyQEQ9BsKBgjFARD0GwoGCMYBEPMbCgYIxwEQ8hsKBgjIARD0GxI_DYFsMXASOAoGCMoBEPQbCgYIkwEQ8hsKBgjJARD0GwoGCMUBEPQbCgYIxgEQ8xsKBgjHARDyGwoGCMgBEPQb; _chartbeat2=.1759838185119.1759840121840.1.ClI00QDbY1YiDfVZU_18MujDAsMFH.3; cnx_userId=3-669c2562654041949e2e499500bd5dbd; _awl=2.1759840128.5-96ae508adb809cf40ba76d184b4f7ea5-6763652d6575726f70652d7765737431-0; _v__chartbeat3=CCPo6ND8Zjq7DvxIfi; cto_bundle=57qa8l9hTSUyQmh3RjZZbzFDMlRueUh1VWdOZ2JLSU1ycGVkTmVhbk9NQ0lPNnJsM1Rua3h6UGRtM3pnS0puNE9pN004TUpnVFBwYkdnZDZVMHJxUDNRMk43Nm5BJTJCb2NWcjRWZnhLVlclMkY4JTJGYjlvOUd1N3lLQU04RUhnS2VvSUszRzJHSTB2VzZ1ZVp5bFpKWkI3S0FiNWhZU3NNQSUzRCUzRA; cto_bidid=z4Q8R19UanREJTJGMll3ZEt5OGJIa1g1WGNVWFZoVFdrTUw3ckdiUCUyRlliN053SDA2UGc5aTdseVdhV1dyUjZuenJqOXZ1dlFONWUzOGhpQXlYY1ZFOHVlWVlFaTBtaWFwZkVQQ3R1JTJGejVoWk41aDhvVSUzRA; reuters-geo={"country":"-", "region":"-"}; datadome=sGRxV~I1MCP3AnRPWEL9f7ovQxIYNO3cfKIAmN26sfg_iTx_y176jcLG8EN91VWPIJoDoK3ODNnNjOKPthbocITWyz2Z2wdz9~zJUGCTjoFMB~Qjc7BnYBi5v7ZZtkg_; __gads=ID=42430803fdf04f31:T=1759838183:RT=1759840421:S=ALNI_Mbrg1xRQ2CwifhZjLKMDqVUF9cuqQ; __gpi=UID=000012471f0045ed:T=1759838183:RT=1759840421:S=ALNI_MbkCPZ_Z0lXLpTfeuCBPtJGGrMbRw; __eoi=ID=f072cd82373d3375:T=1759838183:RT=1759840421:S=AA-AfjYhiLM4FbQ8V2l4jPr9YBA6; _v__SUPERFLY_lockout=1; _dd_s=expire=1759843833402'
}

articles = Article.objects.filter(content__isnull=True)  

for article in articles:
    try:
        print(f"🔄 Loading: {article.title}")
        response = requests.get(article.canonical_url, headers=headers)
        if response.status_code != 200:
            print(f"Ошибка загрузки: {article.canonical_url}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find('div', class_ ='article-body-module__content__bnXL1')
        full_text = paragraphs.get_text(strip=True)

        print(full_text)
        article.content = full_text
        article.save()
        print("✅ Saved")

    except Exception as e:
        print(f"🚨 Error while processing {article.canonical_url}: {e}")
