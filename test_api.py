import torcp_api

def test_api():
    web = torcp_api.app.test_client()

    rv = web.post('/torcpapi', data={'src_path': '../test/', 'dst_path': '../test/result', 'single':'1'})
    print(rv)



if __name__ == '__main__':
    test_api()    