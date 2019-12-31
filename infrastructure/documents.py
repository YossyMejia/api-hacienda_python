import json
from extensions import mysql


def get_document(key_mh):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_getDocumentByKey', (key_mh,))
        row_headers = [x[0] for x in cursor.description]
        data = cursor.fetchall()
        if len(data) is not 0:
            conn.commit()
            json_data = []
            for row in data:
                json_data.append(dict(zip(row_headers, row)))
            return json_data
        else:
            return {'error': 'Error: Not get information of the document'}
    except Exception as e:
        return {'error': str(e)}
    finally:
        cursor.close()
        conn.close()


def get_documents(company_id, state):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_getDocumentByCompany', (company_id, state))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return True
        else:
            return json.dumps({'error': str(data[0])})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


def get_documents(state):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_getDocuments', state)
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return True
        else:
            return json.dumps({'error': str(data[0])})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


def save_document(company_id, key_mh, sign_xml, status, date, document_type, receiver_type, receiver_dni,
                  total_document, total_taxed, pdf=None):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_saveDocument', (company_id, key_mh, sign_xml, status, date, document_type,receiver_type,
                                            receiver_dni, total_document, total_taxed, pdf))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return True
        else:
            return json.dumps({'error': str(data[0])})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


def update_document(company_id, key_mh, answer_xml, status, date):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_updateDocument', (company_id, key_mh, answer_xml, status, date))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return True
        else:
            return json.dumps({'error': str(data[0])})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()
