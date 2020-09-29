import json
from infrastructure import dbadapter as dba
from helpers.errors.enums import DBErrorCodes
from helpers.errors.exceptions import DatabaseError


def save_document(company_id, key_mh, sign_xml, status, date, document_type, receiver,
                  total_document, total_taxed, pdf, email, email_costs, connection=None):
    receiver_type = None
    receiver_dni = None
    if receiver is not None:
        receiver_type = receiver['tipoIdentificacion']
        receiver_dni = receiver['numeroIdentificacion']

    procedure = 'sp_saveDocument'
    args = (company_id, key_mh, sign_xml, status, date, document_type,receiver_type,
                                            receiver_dni, total_document, total_taxed, pdf, email, email_costs)

    try:
        dba.execute_proc(proc_name=procedure, args=args,
                         conn=connection, assert_unique=True)
    except dba.DbAdapterError as dbae:
        raise DatabaseError(dbae.get_message(),
                                 status=DBErrorCodes.DB_DOCUMENT_CREATE) from dbae

    return True



def save_document_line_info(id_company, line_number, quantity, unity
                            , detail, unit_price, net_tax, total_line, key_mh, connection=None):
    procedure = 'sp_createDocumentLineInfo'
    args = (id_company, line_number, quantity, unity
                                                      , detail, unit_price, net_tax, total_line, key_mh)
    try:
        dba.execute_proc(proc_name=procedure,args=args,conn=connection,assert_unique=True)
    except dba.DbAdapterError as dbae:
        raise DatabaseError(dbae.get_message(),
                                status=DBErrorCodes.DB_DOCUMENT_DETAIL_LINE_CREATE) from dbae

    return True



def save_document_line_taxes(id_company, line_number, rate_code, code, rate, amount, key_mh, connection=None):
    procedure = 'sp_createDocumentTaxInfo'
    args = (id_company, line_number, rate_code
                                                     , code, rate, amount, key_mh)
    try:
        dba.execute_proc(proc_name=procedure, args=args, conn=connection,assert_unique=True)
    except dba.DbAdapterError as dbae:
        raise DatabaseError(dbae.get_message(),
                                status=DBErrorCodes.DB_DOCUMENT_LINE_TAX_CREATE) from dbae

    return True



def save_document_additional_email(key_mh, email, connection=None):
    procedure = 'usp_insert_documentxemail'
    args = (key_mh, email)
    try:
        dba.execute_proc(proc_name=procedure, args=args,
                         conn=connection, assert_unique=True)
    except dba.DbAdapterError as dbae:
        raise DatabaseError(dbae.get_message(),
                                status=DBErrorCodes.DB_DOCUMENT_ADDITIONAL_EMAIL_CREATE) from dbae

    return True



def update_document(company_id, key_mh, answer_xml, status, date):
    procedure = 'sp_updateDocument'
    args = (company_id, key_mh, answer_xml, status, date)
    try:
        dba.execute_proc(proc_name=procedure,args=args,
                         assert_unique=True)
    except dba.DbAdapterError as dbae:
        raise DatabaseError(dbae.get_message(),
                                status=enums.DBErrorCodes.DB_DOCUMENT_UPDATE) from dbae

    return True



def get_document(key_mh):
    procedure = 'sp_getDocumentByKey'
    args = (key_mh,)
    try:
        return dba.fetchone_from_proc(procname=procedure, args=args)
    except dba.DbAdapterError as dbae:
        raise DatabaseError(status=DBErrorCodes.DB_DOCUMENT_SELECT_ONE) from dbae



def get_documents(company_id, state): # wtf is this? MARKED FOR DEATH
    procedure = 'sp_getDocumentByCompany'
    args = (company_id, state)
    return dba.fetchall_from_proc(procname=procedure,args=args)



def get_documents(state): # and this???  MARKED FOR DEATH
    procedure = 'sp_getDocuments'
    args = (state,)
    docs = dba.fetchall_from_proc(procname=procedure,args=args)
    if isinstance(docs, dict):
        if '_error' in docs:
            raise dba.DbAdapterError('A problem occurred when attempting to fetch documents by their state.')
        elif '_warning' in docs:
            return []

    return True



def get_documentsreport(company_id, document_type):
    procedure = 'sp_getDocumentsReport'
    args = (company_id, document_type)
    try:
        return dba.fetchall_from_proc(procname=procedure,args=args)
    except dba.DbAdapterError as dbae:
        raise DatabaseError(status=DBErrorCodes.DB_DOCUMENT_SELECT_BY_COMPANY_AND_TYPE) from dbae



def get_additional_emails(key_mh):
    procedure = 'usp_selectByDocKey_documentxemail'
    args = (key_mh,)
    try:
        return dba.fetchall_from_proc(procname=procedure, args=args)
    except dba.DbAdapterError as dbae:
        raise DatabaseError(status=DBErrorCodes.DB_DOCUMENT_SELECT_ADDITIONAL_EMAILS_BY_KEY) from dbae
