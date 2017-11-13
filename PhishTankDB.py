import urllib.request

class PhishTank:

	def __init__(self):

		# API key for VasiqMz
		self.api_key = '<api key>'

		# Base URL for phishtank
		self.base_url = 'http://data.phishtank.com/data/'
		# the file to fetch from PhishTank
		self.phishtank_dbfile = '/online-valid.csv'

		# URL handler for downloading the PhishTank DB
		self.url_handler = None

	# Generates the URL required to fetch the 
	# updated DB from the PhishTank site 	
	def gen_db_fetch_url(self):

		# As per PhishTank to fetch the DB file multiple times a day
		# putting the API key in the URL would help
		# and the format of the URL must be as followed
		# http://data.phishtank.com/data/<>/online-valid.csv.bz2

		if len(self.base_url) != 0 and len(self.phishtank_dbfile) != 0:
			return self.base_url+self.api_key+self.phishtank_dbfile


	# Perform a HEAD req to the PhishTank
	# this will help to understand if there's a need
	# to download the new updated DB or not ..		
	def do_head_req_phishtank(self, req_url):

		# Request object with HEAD as a request ...
		req_handler = urllib.request.Request(req_url, method='HEAD')
		try:
			resp_handler = urllib.request.urlopen(req_handler)
		except Exception as e:
			print('Exception has occurred ...')
			print(e)
			# Close the above 2 handlers now ... as they are local 
			# to the function 
			resp_handler.close()
			req_handler.close()

		# Fetches the ETag value and return it for further analysis	
		return resp_handler.info().get('ETag')

	# Requesting from the PhishTank to get the updated DB	
	def req_phistank_db(self, dl_url):
		try:
			# Check the ETag first to see if the DB has been updated or not
			if not self.is_phishtankdb_updated(self.do_head_req_phishtank(dl_url)):
				# So the ETag has changed ... now need to download the new DB
				print('PhishTank DB not updated ... hence downloading the new one ...')
				self.url_handler = urllib.request.urlopen(dl_url)
				self.dl_phishtank_db()
			else:
				print('DB is updated already ... ')

			self.close_req()

		except Exception as e:
			print('Exception has occurred ...')
			print(e)
			self.close_req()

	# Close any open request 		
	def close_req(self):
		if self.url_handler != None:
			self.url_handler.close()

	# Using the latest ETag that we received from HEAD req
	# the func will perform a comparision between the one
	# stored in the file ...		
	def is_phishtankdb_updated(self, latestetag):

		last_etag = self.get_last_etag()
		print('The last etag is '+str(last_etag))
		print('The latest etag is '+str(latestetag))
		if last_etag == latestetag:
			return True
		else:
			print('Etag needs to be updated now ...')
			self.write_etag(latestetag)
			return False	


	# Fetches the latest ETag from the file ...		
	def get_last_etag(self, filename='phishtank-etag'):

		etag_handler = open(filename, 'r')
		last_etag = etag_handler.read()
		etag_handler.close()
		return last_etag

	# writing the latest etag to the file for future ref.	
	def write_etag(self, latest_etag, filename='phishtank-etag'):

		etag_handler = open(filename, 'w')
		etag_handler.write(latest_etag)
		etag_handler.close()

		print('Etag has been updated ...')

	# downloading the updated PhishTank DB and storing it ...	
	def dl_phishtank_db(self, localfilename='online-valid.csv.bz2'):

		try:
			dbfile_handler = open(localfilename, 'b+w')
			dbfile_handler.write(self.url_handler.read())
		except Exception as e:
			print('Exception has occurred ...')
			print(e)

		print('File has been downloaded ...')	
		dbfile_handler.close()	


	#def check_etag(self, curr_etag)

a = PhishTank()
a.req_phistank_db(a.gen_db_fetch_url())