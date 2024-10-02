from django.http import HttpResponse
import re

# def index(request):
#     return HttpResponse("Hello, world. You're at the CIS index.")



from django.shortcuts import render
from django.db import connections
from django.views import View

def index(request):
    # Use the default connection for production data
    with connections['default'].cursor() as prod_cursor:
        prod_cursor.execute("SELECT C_DATAVERSION, C_SYSTEMID, C_APPDICTPATCH FROM CIS4PROD.ADVANCED.SYS001")
        sys001_prod_data = prod_cursor.fetchall()
        
        prod_cursor.execute("SELECT C_ATTACHMENTSFOLDER, C_LETTERSFOLDER, C_BILLIMAGEFOLDER, C_HELPURL FROM CIS4PROD.ADVANCED.BIF000")
        bif000_prod_data = prod_cursor.fetchall()
        
        prod_cursor.execute(f"SELECT C_LINKTYPE, C_FILENAME FROM CIS4PROD.ADVANCED.SYS021 WHERE C_LINKTYPE IN ('REFUNDCHK','GL')")
        sys021_prod_data = prod_cursor.fetchall()
        
        prod_cursor.execute(f"SELECT  COUNT(*) users FROM CIS4PROD.ADVANCED.SYS010")
        sys010_prod_data = prod_cursor.fetchall()
        
        prod_cursor.execute(f"SELECT  COUNT(*) users FROM CIS4PROD.ADVANCED.SYS010 WHERE L_DISABLED = 0")
        num_users_prod = prod_cursor.fetchall()
        
        prod_cursor.execute(f"SELECT C_CODE, SUBSTRING(C_CONFIGURATION, CHARINDEX('<FileName Type=\"Script\">', C_CONFIGURATION), ABS(CHARINDEX('</FileName>', C_CONFIGURATION) - CHARINDEX('<FileName Type=\"Script\">', C_CONFIGURATION))) AS URL FROM CIS4PROD.ADVANCED.ITR028 WHERE C_CONFIGURATION LIKE '%CIS4%'")
        itr_prod_data = prod_cursor.fetchall()
        
        prod_cursor.execute(f"SELECT COUNT(1) from CIS4PROD.ADVANCED.SYS002")
        current_prod_login_users = prod_cursor.fetchall()


        


        
    # Use the test connection for test data
    with connections['cis_test'].cursor() as test_cursor:
        test_cursor.execute("SELECT C_DATAVERSION, C_SYSTEMID, C_APPDICTPATCH FROM CIS4TEST.ADVANCED.SYS001")
        sys001_test_data = test_cursor.fetchall()
        
        test_cursor.execute("SELECT C_ATTACHMENTSFOLDER, C_LETTERSFOLDER, C_BILLIMAGEFOLDER, C_HELPURL FROM CIS4TEST.ADVANCED.BIF000")
        bif000_test_data = test_cursor.fetchall()
        
        test_cursor.execute("SELECT C_LINKTYPE, C_FILENAME FROM CIS4TEST.ADVANCED.SYS021 WHERE C_LINKTYPE IN ('REFUNDCHK','GL')")
        sys021_test_data = test_cursor.fetchall()
        
        test_cursor.execute(f"SELECT  COUNT(*) users FROM CIS4TEST.ADVANCED.SYS010")
        sys010_test_data = test_cursor.fetchall()
        
        test_cursor.execute(f"SELECT  COUNT(*) users FROM CIS4TEST.ADVANCED.SYS010 WHERE L_DISABLED = 0")
        num_users_test = test_cursor.fetchall()
        
        test_cursor.execute(f"SELECT C_CODE, SUBSTRING(C_CONFIGURATION, CHARINDEX('<FileName Type=\"Script\">', C_CONFIGURATION), ABS(CHARINDEX('</FileName>', C_CONFIGURATION) - CHARINDEX('<FileName Type=\"Script\">', C_CONFIGURATION))) AS URL FROM CIS4TEST.ADVANCED.ITR028 WHERE C_CONFIGURATION LIKE '%CIS4%'")
        itr_test_data = test_cursor.fetchall()
        
        test_cursor.execute(f"SELECT COUNT(1) from CIS4TEST.ADVANCED.SYS002")
        current_test_login_users = test_cursor.fetchall()
     

        
    return render(request, 
                  'webapp/index.html', 
                  {
                      'sys001_prods': sys001_prod_data,
                      'sys001_tests': sys001_test_data,
                      'bif000_prods': bif000_prod_data,
                      'bif000_tests': bif000_test_data,
                      'sys021_prods': sys021_prod_data,
                      'sys021_tests': sys021_test_data,
                      'sys010_prods': sys010_prod_data,
                      'sys010_tests': sys010_test_data,
                      'itr_prods': itr_prod_data,
                      'itr_tests': itr_test_data,
                      'num_users_prod': num_users_prod,
                      'num_users_test': num_users_test,
                      
                      'current_prod_login_users': current_prod_login_users,
                      'current_test_login_users': current_test_login_users,
                  })         
    
    
class LoginDetailsView(View):
    def get(self, request):
        with connections['default'].cursor() as prod_cursor:
            prod_cursor.execute(f"SELECT C_USERID, T_LOGIN, C_STATIONID from ADVANCED.SYS002 ORDER BY C_USERID, T_LOGIN DESC")
            current_prod_login_users = prod_cursor.fetchall()
            
        # with connections['test_cis'].cursor() as test_cursor:
        #     test_cursor.execute(f"SELECT C_USERID, T_LOGIN, C_STATIONID from ADVANCED.SYS002 ORDER BY C_USERID, T_LOGIN DESC")
        #     current_test_login_users = test_cursor.fetchall()
        
        return render(request, 'webapp/login_details.html', {
            'current_prod_login_users': current_prod_login_users,
            # 'current_test_login_users': current_test_login_users,
        })
        
class TESTLoginDetailsView(View):
    def get(self, request):
        with connections['cis_test'].cursor() as test_cursor:
            test_cursor.execute(f"SELECT C_USERID, T_LOGIN, C_STATIONID from ADVANCED.SYS002 ORDER BY C_USERID, T_LOGIN DESC")
            current_test_login_users = test_cursor.fetchall()
            
        # with connections['test_cis'].cursor() as test_cursor:
        #     test_cursor.execute(f"SELECT C_USERID, T_LOGIN, C_STATIONID from ADVANCED.SYS002 ORDER BY C_USERID, T_LOGIN DESC")
        #     current_test_login_users = test_cursor.fetchall()
        
        return render(request, 'webapp/login_details_test.html', {
            'current_test_login_users': current_test_login_users,
            # 'current_test_login_users': current_test_login_users,
        })