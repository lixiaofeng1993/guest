# BS = 16
#
# pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
#
# print(pad('sadsda'))
#
#
# from Crypto.Cipher import AES
#

with open('guests.txt', 'w') as f:
    for i in range(1, 3001):
        str_i = str(i)
        realname = 'Tom' + str_i
        phone = 18700000000 + i
        email = 'Tom' + str_i + '@mail.com'
        sql = 'insert into sign_guest (realname, phone, email, sign, event_id) values ("{}", "{}", "{}", 0, 1);'.format(
            realname, phone, email)
        f.write(sql)
        f.write('\n')