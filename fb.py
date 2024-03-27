import re, requests, os, sys
from bs4 import BeautifulSoup as bsp
from datetime import datetime

class login:
	def __init__(self):
		self.token_app = '1348564698517390|007c0a9101b9e1c8ffab727666805038'
		self.data = {}
		self.host = 'https://m.facebook.com'
		self.hitung = 0

	#->> ambi access token
	def GetingCode(self, coki):
		with requests.Session() as r:
			self.r = r.post(f'https://graph.facebook.com/v2.6/device/login?access_token={self.token_app}').json()
			self.user_code, self.code = self.r['user_code'], self.r['code']
			self.r1 = bsp(r.get(f'https://m.facebook.com/device?user_code={self.user_code}', cookies = {'cookie':coki}).text,'html.parser')
			self.ls = ['fb_dtsg','jazoest','qr']
			for self.i in self.r1.find_all('input'):
				if self.i.get('name') in self.ls: self.data.update({self.i['name']:self.i['value']})
			self.data.update({'user_code':self.user_code})
			self.ul = self.r1.find('form', method='post')['action']
			self.r2 = bsp(r.post(self.host + self.ul, data=self.data, cookies = {'cookie':coki}).text,'html.parser')
			self.data.clear()
			for self.a in self.r2.find_all('input'):
				if self.a.get('name') == '__CANCEL__':pass
				else:self.data.update({self.a.get('name','submit'):self.a.get('value')})
			self.r3 = r.post(self.host + self.r2.find('form', method='post')['action'], data=self.data, cookies = {'cookie':coki}).text
			self.r4 = r.post(f'https://graph.facebook.com/v2.6/device/login_status?access_token={self.token_app}&code={self.code}',cookies = {'cookie':coki}).json()['access_token']
			print('\n [+] Token : ',self.r4)
			return self.r4

	def GetAplication(self, cokie, variabel, type, dev='6890604894306710'):
		with requests.Session() as r:
			r.headers.update({
                            'origin': 'https://m.facebook.com',
                            'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 4 Build/NMF26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36 [FBAN/FB4A;FBAV/417.0.0.33.65;FBBV/480086274;FBDM/{density=2.0,width=768,height=1184};FBLC/en_US;FBRV/0;FB_FW/2;FBCR/Android;FBMF/unknown;FBBD/Google;FBPN/com.facebook.katana;FBDV/Nexus 4;FBSV/7.1.1;FBOP/1;FBCA/x86:;]',
                            'viewport-width': '384',
                            'x-fb-friendly-name': 'MAppSettingsOverviewRootViewQuery',
                            'x-asbd-id': '129477',
                            'content-type': 'application/x-www-form-urlencoded',
                            'accept': '*/*',
                            'referer': 'https://m.facebook.com/settings/applications/overview/?paipv=0&eav=AfYeUmYJmBbc1iJnoQUZ-34kU-x4CcW1GiAoEpJSU6Q09alL3tAxTwKw7nBUbpzkNLs&wtsid=rdr_0jTaA9zwsc4u5VES5&_rdr',
                            'accept-language': 'en-US,en;q=0.9',
                            'x-requested-with': 'com.facebook.katana',
                        })
			self.r1 = r.get('https://m.facebook.com/settings/applications/overview/?', cookies={'cookie':cokie}).text
			data = {
                            'av': re.search('c_user=(\d+)', str(cokie)).group(1),
                            '__user': re.search('c_user=(\d+)', str(cokie)).group(1),
                            '__a': '1',
                            '__req': '1',
                            '__hs': '19807.BP:faceweb_pkg.2.0..0.0',
                            'dpr': '2',
                            '__ccg': 'GOOD',
                            '__s': '',
                            '__hsi': re.search('"hsi":"(\d+)"', str(self.r1)).group(1),
                            '__dyn': '',
                            '__csr': '',
                            'fb_dtsg': re.search('{"dtsg":{"token":"(.*?)"', str(self.r1)).group(1),
                            'jazoest': '25581',
                            'lsd': re.search('"LSD",\[\],{"token":"(.*?)"', str(self.r1)).group(1),
                            'fb_api_caller_class': 'RelayModern',
                            'fb_api_req_friendly_name': 'MAppSettingsOverviewRootViewQuery',
                            'variables': variabel,
                            'server_timestamps': 'true',
                            'doc_id': dev
                        }
			self.r2 = r.post('https://m.facebook.com/api/graphql/', data=data,cookies={'cookie':cokie}).json()["data"]
			self.khamd = 'expiredApps' if type == 'exp' else 'activeApps'
			self.aktif = self.r2["viewer"]["actor"][self.khamd]['edges']
			for self.a in self.aktif:
				self.hitung +=1
				self.cek = self.a['node']['apps_and_websites_view']['detailView']
				print(f'''
 [{self.hitung}]

	Nama Aplikasi   : {self.cek['app_name']}
	Di install Pada : {datetime.fromtimestamp(int(self.cek['install_timestamp']))}
	Id Aplikasi     : {self.cek['app_id']}
	Status Aplikasi : {self.cek['app_status']}
	Logo Aplikasi   : {self.cek['logo_url']}''')
			self.next = self.r2['viewer']['actor'][self.khamd]['page_info']['has_next_page']
			if self.next is True:
				self.var = '{"after":"%s","first":%s,"id":"%s"}'%(self.a['cursor'], self.hitung, data['av'])
				if self.kham == 'expiredApps':
					self.GetAplication(cokie, self.var, type, '5018766638215602')
				else:
					self.GetAplication(cokie, self.var, type)
			else:
				self.dihi = 'kadarluarsa' if type == 'exp' else 'aktif'
				print('\n [+] Anda memiliki %s aplikasi %s'%(self.hitung,self.dihi))
	
class menu:
	def __init__(self):
		self.id = []

	def Menu(self):
		os.system('clear' if 'linux' in sys.platform.lower() else 'cls')
		print('\n [1] Get Token EAAT')
		print(' [2] Cek Aplikasi Terkait')
		print(' [3] Dump Friends Unlimited\n')
		while True:
			x = input(' [?] pilih : ')
			if x in ['1','01']:
				print('\n [?] Masukan cookie akun facebook kamu')
				cokie = input(' [?] cookie : ')
				try:login().GetingCode(cokie)
				except:exit('\n [!] Cokie invalid')
			elif x in ['2','02']:
				print('\n [?] Masukan cookie akun facebook kamu, pastikan cokie aktif')
				cokie = input(' [?] cookie : ')
				print('\n [1] Cek aplikasi aktif')
				print(' [2] Cek Aplikasi kadarluarsa\n')
				apk = input(' [?] pilih : ')
				if apk in ['1','01']:
					try:login().GetAplication(cokie,'{"includeRemovedAppId":false,"removedAppId":null}','khamdihidev')
					except:exit('\n [!] Cokie invalid')
				else:
					try:login().GetAplication(cokie,'{"includeRemovedAppId":false,"removedAppId":null}','exp')
					except:exit('\n [!] Cokie invalid')
			elif x in ['3','03']:
				print('\n [?] Masukan cookie akun facebook kamu')
				cokie = input(' [?] cookie : ')
				try:token=login().GetingCode(cokie)
				except:exit('\n [!] Cokie invalid')
				print('\n [!] Masukan userid Gunakan Tanda Koma Sebagai Pemisah')
				userid = input(' [?] ID Target : ')
				for self.x in userid.split(','):
					self.dumps(self.x, cokie, token)
				if len(self.id) == 0:
					exit('\n [!] Gagal Dumps ID')
				self.file = input('\n\n [?] Simpan dump kali ini?\n [?] Masukan nama file : ')
				for self.index, self.value in enumerate(self.id):
					print(' %s. %s'%( self.index, self.value))
					open(self.file,'a').write(f'{self.value}\n')
				print('\n [✓] File Di Simpan di : {}'.format(self.file))
			break

	def dumps(self, id, cokie, token):
		try:
			self.req = requests.get('https://graph.facebook.com/%s?fields=id,name,friends&access_token=%s'%(id, token), cookies = {'cookie':cokie}).json()
			self.id.append(self.req['id']+'|'+self.req['name'])
			for self.y in self.req['friends']['data']:
				if self.y['id'] not in str(self.id): self.id.append(self.y['id']+'|'+self.y['name'])
				print('\r [+] Success dump : %s'%(len(self.id)),end=' ')
		except:pass
menu().Menu()
