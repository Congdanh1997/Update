class Main():
    def update_progessbar(self, value):
      self.uic.progressBar.setValue(value)
      if value == 100:
          self.uic.lb_update.setText("Đã Tải File Update.rar")
    def thread_checkversion(self):
      t = threading.Thread(target=self.checkversion)
      t.start()
    def checkversion(self):
        self.uic.update_tool.setEnabled(False)
        self.uic.lb_update.show()
        self.uic.lb_update.setText("Checking Version")
        getversion = self.get_version().replace("\n", "")
        if version.parse(ver) < version.parse(getversion):
            self.uic.lb_update.setText("Đang Update")
            self.uic.progressBar.show()
            self.uic.tmproxy_cb.hide()
            self.uic.kiotproxy.hide()
            self.uic.wwproxy.hide()
            self.uic.connectsock.hide()
            self.uic.mobile_cb.hide()
            self.thead_update = Download_Tool(index=0)
            self.thead_update.process_signal.connect(self.update_progessbar)
            self.thead_update.start()
        else:
            self.uic.lb_update.setText("Chưa Có Bản Update")
            self.uic.update_tool.setEnabled(True)
            sleep(2)
            self.uic.lb_update.hide()
            print("Bản Mới Nhất")

class Download_Tool(QThread):
        process_signal = pyqtSignal(object)
        def __init__(self, index=0):
            super(Download_Tool, self).__init__()
            self.file_id = "1Yj7wEVhzE0bz7lJ8gY_XnCQOo0vmzg0O"
            self.destination = "Update.rar"
            self.total_size = 0
            self.index = index
        def get_file_size(self):
            URL = "https://drive.google.com/uc?export=download"
            session = requests.Session()
            response = session.head(URL, params={'id': self.file_id}, allow_redirects=True)
            if 'Content-Length' in response.headers:
                self.total_size = int(response.headers['Content-Length'])
            else:
                print("Content-Length header not found.")
        def download_file_from_google_drive(self):
            URL = "https://drive.google.com/uc?export=download"
            session = requests.Session()
            response = session.get(URL, params={'id': self.file_id}, stream=True)
            token = self.get_confirm_token(response)
            print(token)
            if token:
                params = {'id': self.file_id, 'confirm': token}
                response = session.get(URL, params=params, stream=True)
            self.save_response_content(response)
        def get_confirm_token(self, response):
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    return value
            return None
        def save_response_content(self, response):
            CHUNK_SIZE = 32768
            offset = 0
            with open(self.destination, "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        offset = offset + len(chunk)
                        process = (offset / self.total_size) * 100
                        self.process_signal.emit(int(process))
        def run(self):
            self.get_file_size()
            self.download_file_from_google_drive()
