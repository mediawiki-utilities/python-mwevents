from ..lib import dictish
from .change import Change, INDEFINITE, try_keys


class Revised(Change):
	
	matches = [
		Match(None, None, True)
	]
	
	def __init__(self, id, user, page, bot, minor, diff, sha1, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.id    = int(id)
		self.user  = User(user)
		self.page  = Page(page)
		self.diff  = Diff(diff)
		self.bot   = bool(bot)
		self.minor = bool(minor)
		self.sha1  = str(sha1)
		
		super().register(self)
		
	@classmethod
	def from_api(cls, doc):
		"""
		:Example API doc::
			{
				"type": "edit",
				"ns": 1,
				"title": "Talk:Neutral mutation",
				"rcid": 616266829,
				"pageid": 5555386,
				"revid": 581269873,
				"old_revid": 581268750,
				"user": "Grabriggs",
				"userid": "19701352",
				"oldlen": 23767,
				"newlen": 24046,
				"timestamp": "2013-11-12T01:48:22Z",
				"comment": "/* Neutral theory */",
				"tags": [],
				"sha1": "8817b4efd42c936254dfb09ce5bbfd0e4f9b848a"
			}
		"""
		ns, title = Page.parse_title(doc['title'])
		assert ns == doc['ns']
		
		return cls(
			doc['revid'],
			User(
				int(doc['userid']),
				doc['user']
			),
			Page(
				doc['pageid'],
				old_ns,
				old_title
			),
			Diff(
				doc['oldlen'],
				doc['newlen']
			),
			'bot' in doc,
			'minor' in doc,
			'new' in doc,
			doc['sha1'],
			doc['rcid'],
			doc['timestamp'],
			doc['comment']
		)
	
	@classmethod
	def from_db(cls, row):
		"""
		:Example DB row::
			+-----------+----------------+-------------+----------+---------------+--------------+-------------------------+-------------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+----------------+------------+------------+------------+----------+-------------+---------------+-----------+
			| rc_id     | rc_timestamp   | rc_cur_time | rc_user  | rc_user_text  | rc_namespace | rc_title                | rc_comment        | rc_minor | rc_bot | rc_new | rc_cur_id | rc_this_oldid | rc_last_oldid | rc_type | rc_source | rc_moved_to_ns | rc_moved_to_title | rc_patrolled | rc_ip          | rc_old_len | rc_new_len | rc_deleted | rc_logid | rc_log_type | rc_log_action | rc_params |
			+-----------+----------------+-------------+----------+---------------+--------------+-------------------------+-------------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+----------------+------------+------------+------------+----------+-------------+---------------+-----------+
			| 624362534 | 20131219020516 |             | 16380370 | RedVanderwall |            0 | Narragansett_Race_Track | /* The Biscuit */ |        1 |      0 |      0 |  10680758 |     586726430 |     586725822 |       0 | mw.edit   |              0 |                   |            0 | 71.174.171.233 |      24309 |      24348 |          0 |        0 | NULL        |               |           |
			+-----------+----------------+-------------+----------+---------------+--------------+-------------------------+-------------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+----------------+------------+------------+------------+----------+-------------+---------------+-----------+
		"""
		
		cls(
			row['rc_this_oldid'],
			User(
				row(row['rc_user']),
				row['rc_user_text']
			),
			Page(
				row['rev_id'],
				row['rc_namespace'],
				row['rc_title']
			),
			Diff(
				row['rc_old_len'],
				row['rc_new_len']
			),
			row['rc_bot'] > 0,
			row['rc_minor'] > 0,
			row['rc_new'] > 0,
			row['rev_sha1'],
			row['rc_id'],
			row['timestamp'],
			row['comment']
		)
	

class Moved(LogEvent):
	
	matches = [
		Match("move", "move", False)
	]
	
	
	def __init__(self, user, old_ns, old_title, new_ns, new_title, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.old_ns = int(old_ns)
		self.old_title = str(old_title)
		self.new_ns = int(new_ns)
		self.new_title = str(new_title)
		
		super().register(self)
		

		



class Deleted(LogEvent):
	
	matches=[
		Match("delete", "delete", False)
	]
	
	
	def __init__(self, user, page_ns, page_title, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.page_ns    = int(page_ns)
		self.page_title = int(page_title)
		
		super().register(self)
		
	




class Restored(LogEvent):
	
	matches=[
		Match("delete", "restore", False)
	]
	
	def __init__(self, user, page, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.user = User(user)
		self.page = Page(page)
		
		super().register(self)
		
	@classmethod
	def from_api(cls, doc):
		"""
		:Example API doc::
			{
				"type": "log",
				"ns": 3,
				"title": "User talk:Envisage Drawn",
				"rcid": 616228397,
				"pageid": 41053035,
				"revid": 0,
				"old_revid": 0,
				"user": "Peridon",
				"userid": "7128128",
				"oldlen": 0,
				"newlen": 0,
				"timestamp": "2013-11-11T22:01:52Z",
				"comment": "1 revision restored: wrong button!",
				"logid": 52553202,
				"logtype": "delete",
				"logaction": "restore",
				"tags": []
			}
		"""
		ns, title = Page.parse_title(doc['title'])
		assert ns == doc['ns']
		
		return cls(
			User(
				int(doc['userid']),
				doc['user']
			),
			Page(
				doc['pageid'],
				ns,
				title
			),
			doc['logid'],
			doc['rcid'],
			doc['timestamp'],
			doc['comment'],
			rc_id=doc['rcid']
		)
	
	@classmethod
	def from_db(cls, row):
		"""
		:Example DB row::
			+-----------+----------------+-------------+---------+--------------+--------------+------------+---------------------------------------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+---------------+------------+------------+------------+----------+-------------+---------------+-----------+
			| rc_id     | rc_timestamp   | rc_cur_time | rc_user | rc_user_text | rc_namespace | rc_title   | rc_comment                                  | rc_minor | rc_bot | rc_new | rc_cur_id | rc_this_oldid | rc_last_oldid | rc_type | rc_source | rc_moved_to_ns | rc_moved_to_title | rc_patrolled | rc_ip         | rc_old_len | rc_new_len | rc_deleted | rc_logid | rc_log_type | rc_log_action | rc_params |
			+-----------+----------------+-------------+---------+--------------+--------------+------------+---------------------------------------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+---------------+------------+------------+------------+----------+-------------+---------------+-----------+
			| 624359907 | 20131219014436 |             | 7181920 | OlEnglish    |            0 | Jelly_Jamm | 11 revisions restored: userfied per request |        0 |      0 |      0 |  41404991 |             0 |             0 |       3 | mw.log    |              0 |                   |            1 | 184.65.77.154 |       NULL |       NULL |          0 | 53586897 | delete      | restore       | a:0:{}    |
			+-----------+----------------+-------------+---------+--------------+--------------+------------+---------------------------------------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+---------------+------------+------------+------------+----------+-------------+---------------+-----------+
			1 row in set (0.05 sec)
		"""
		return cls(
			User(
				int(row.get('log_user', row.get('rc_user'))),
				row['rc_user_text']
			),
			Page(
				row['log_page'],
				row.get('log_namespace', row['rc_namespace']),
				row['rc_title']
			),
			row['rc_logid'],
			row['rc_id'],
			row['rc_timestamp'],
			row['rc_comment'],
			rc_id=row['rc_id']
		)
			
	
class Protect(LogEvent):
	
	matches=[
		Match("protect", "protect", False)
	]
	
	def __init__(self, page, param, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		
		self.page    = Page(page)
		self.param   = str(param)
	
	@classmethod
	def from_api(cls, doc, title_parser=None):
		"""
		:Example API doc::
			{
				"type": "log",
				"ns": 0,
				"title": "Alice (Avril Lavigne song)",
				"rcid": 616736350,
				"pageid": 25727375,
				"revid": 0,
				"old_revid": 0,
				"user": "Mark Arsten",
				"userid": "15020596",
				"oldlen": 0,
				"newlen": 0,
				"timestamp": "2013-11-14T03:20:35Z",
				"comment": "Persistent IP edit warring",
				"logid": 52608670,
				"logtype": "protect",
				"logaction": "protect",
				"0": "\u200e[edit=autoconfirmed] (expires 03:20, 21 November 2013 (UTC))",
				"1": "",
				"tags": []
			}
		"""
		ns, title = title_parser.parse(doc['title'])
		assert ns == doc['ns']
		return cls(
			Page(
				doc['pageid'],
				doc['ns'],
				title
			),
			doc.get('0'),
			doc['logid'],
			doc['rcid'],
			doc['timestamp'],
			doc['comment']
		)
		
	@classmethod
	def from_db(cls, row, title_parser=None, ):
		"""
		:Example DB row::
			+-----------+----------------+-------------+---------+--------------+--------------+--------------+----------------------------------------------------------------------------------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+----------------+------------+------------+------------+----------+-------------+---------------+---------------------------------+
			| rc_id     | rc_timestamp   | rc_cur_time | rc_user | rc_user_text | rc_namespace | rc_title     | rc_comment                                                                             | rc_minor | rc_bot | rc_new | rc_cur_id | rc_this_oldid | rc_last_oldid | rc_type | rc_source | rc_moved_to_ns | rc_moved_to_title | rc_patrolled | rc_ip          | rc_old_len | rc_new_len | rc_deleted | rc_logid | rc_log_type | rc_log_action | rc_params                       |
			+-----------+----------------+-------------+---------+--------------+--------------+--------------+----------------------------------------------------------------------------------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+----------------+------------+------------+------------+----------+-------------+---------------+---------------------------------+
			| 624359365 | 20131219014049 |             | 3072955 | Kelapstick   |            0 | Misterduncan | repeatedly created [[WP:CSD#A7|A7]] article − non-notable person, organisation, etc.   |        0 |      0 |      0 |         0 |             0 |             0 |       3 | mw.log    |              0 |                   |            1 | 207.231.234.23 |       NULL |       NULL |          0 | 53586837 | protect     | protect       | ‎[create=sysop] (indefinite)     |
			+-----------+----------------+-------------+---------+--------------+--------------+--------------+----------------------------------------------------------------------------------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+----------------+------------+------------+------------+----------+-------------+---------------+---------------------------------+
		"""
		return cls(
			Page(
				try_keys(row, ['log_page', 'rc_page']),
				try_keys(row, ['log_namespace', 'rc_namespace']),
				try_keys(row, ['log_title', 'rc_title'])
			),
			try_keys(row, ['log_params', 'rc_params']),
			try_keys(row, ['log_id', 'rc_logid']),
			row.get('rc_id'),
			try_keys(row, ['log_timestamp', 'rc_timestamp']),
			try_keys(row, ['log_comment', 'rc_comment'])
		)
	
	
class Unprotect(LogEvent):
	"""
	Processes represents an action that removes the 'protected' status of a
	page.
	"""
	
	matches=[
		Match("protect", "unprotect", False)
	]
	
	def __init__(self, page, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		
		self.page    = Page(page)
	
	@classmethod
	def from_api(cls, doc, title_parser):
		"""
		:Example API doc::
			{
				"type": "log",
				"ns": 6,
				"title": "File:ElmerFlick.jpg",
				"rcid": 616706496,
				"pageid": 986245,
				"revid": 0,
				"old_revid": 0,
				"user": "DYKUpdateBot",
				"userid": "11745509",
				"bot": "",
				"oldlen": 0,
				"newlen": 0,
				"timestamp": "2013-11-14T00:05:14Z",
				"comment": "File off the [[T:DYK|DYK]] section of the Main Page",
				"logid": 52605770,
				"logtype": "protect",
				"logaction": "unprotect",
				"tags": []
			}
		"""
		ns, title = title_parser.parse(doc['title'])
		assert ns == doc['ns']
		return cls(
			Page(
				doc['pageid'],
				doc['ns'],
				title
			),
			doc['logid'],
			doc['rcid'],
			doc['timestamp'],
			doc['comment']
		)
	
	@classmethod
	def from_db(cls, row):
		"""
		:Example DB row::
			+-----------+----------------+----------------+----------+--------------+--------------+---------------------+------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+---------------+------------+------------+------------+----------+-------------+---------------+-----------+
			| rc_id     | rc_timestamp   | rc_cur_time    | rc_user  | rc_user_text | rc_namespace | rc_title            | rc_comment | rc_minor | rc_bot | rc_new | rc_cur_id | rc_this_oldid | rc_last_oldid | rc_type | rc_source | rc_moved_to_ns | rc_moved_to_title | rc_patrolled | rc_ip         | rc_old_len | rc_new_len | rc_deleted | rc_logid | rc_log_type | rc_log_action | rc_params |
			+-----------+----------------+----------------+----------+--------------+--------------+---------------------+------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+---------------+------------+------------+------------+----------+-------------+---------------+-----------+
			| 617835058 | 20131119154437 | 20131119154437 | 15020596 | Mark Arsten  |            0 | Miss_Universe_2014* |            |        0 |      0 |      0 |         0 |             0 |             0 |       3 | mw.log    |              0 |                   |            1 | 24.63.113.173 |       NULL |       NULL |          0 | 52731579 | protect     | unprotect     |           |
			+-----------+----------------+----------------+----------+--------------+--------------+---------------------+------------+----------+--------+--------+-----------+---------------+---------------+---------+-----------+----------------+-------------------+--------------+---------------+------------+------------+------------+----------+-------------+---------------+-----------+
			1 row in set (0.38 sec)
		"""
		return cls(
			Page(
				try_keys(row, ['log_page']),
				try_keys(row, ['log_namespace', 'rc_namespace']),
				try_keys(row, ['log_title', 'rc_title'])
			),
			try_keys(row, ['log_id', 'rc_logid']),
			row.get('rc_id'),
			try_keys(row, ['log_timestamp', 'rc_timestamp']),
			try_keys(row, ['log_comment', 'rc_comment']),
		)
