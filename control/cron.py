from .models import ScConditionsResult
from .models import ScUsers, ScPaths, ScResults, ScConditions, ScConditionsOnline
from datetime import datetime, timedelta
from django.utils import timezone
import time
import re
import json
import SQLParser.xxxdbrc
import pymysql as MySQLdb


# connection FOR PRODUCTION
# def get_connection_journal_db():
#     config = SQLParser.xxxdbrc.config('journal')
#     connection = MySQLdb.connect(host=config["hostname"],
#                                  user=config["username"],
#                                  passwd=config["password"],
#                                  db=config["dbname"],
#                                  port=config["port"],
#                                  charset='utf8')
#     cursor = connection.cursor(MySQLdb.cursors.DictCursor)
#     return cursor, connection


def get_connection_journal_db():
    connection = MySQLdb.connect(host='localhost',
                                 user='test_admin',
                                 passwd='test_admin',
                                 db='OnlWeblog',
                                 port=3306,
                                 charset='utf8')
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    return cursor, connection


def close_connection_journal_db(cur, conn):
    cur.close()
    conn.close()
    print('Connection is closed')


def get_vars_formula(formula):
    x = re.findall(
        "(([A-Za-z0-9_]+):((?:\\.|[A-Za-z0-9_.\-\/\ ])+):([A-Za-z0-9_]+)(?:\(([+-]?\d+)([a-z]+)(?:,([+-]?\d+)([a-z]+))\))?)",
        formula)
    vars_formula = list()
    for i in range(len(x)):
        vars_formula.append(x[i][0])
    return vars_formula


def update_condition_results():
    ids_for_signal_alarm = list()
    global bool_result
    '''Время волшебства'''
    data = ScConditionsOnline.objects.all()
    for condition in data:
        formula = condition.formula
        vars_formula = get_vars_formula(formula)
        empty_values = list()
        for var_formula in vars_formula:
            formula = formula.replace(str(var_formula),
                                      str(ScResults.objects.filter(var_title=var_formula)[0].value))
            helper = str(ScResults.objects.filter(var_title=var_formula)[0].comment)
            if helper == 'Empty' or helper == 'DB error' or helper == "Can't get process":
                empty_values.append(str(ScResults.objects.filter(var_title=var_formula)[0].var_title))
        digit_formula = formula
        if empty_values:
            result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=formula,
                                               empty_values=str(empty_values), text_formula=condition.formula,
                                               time_calc=(datetime.now(tz=timezone.utc)))
            result_for_db.save()
        else:
            result = eval(digit_formula)
            if condition.cond_type == '7':
                bool_result = bool(result)
                if not bool_result and condition.display_method == 'Text+Siren':
                    ids_for_signal_alarm.append(condition.cond_id)
                result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=formula,
                                                   bool_result=bool_result, text_formula=condition.formula,
                                                   time_calc=(datetime.now(tz=timezone.utc)))
                result_for_db.save()
            if condition.cond_type == '1':
                result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=formula,
                                                   val_result=result,
                                                   text_formula=condition.formula,
                                                   time_calc=(datetime.now(tz=timezone.utc)))
                result_for_db.save()
            if condition.cond_type == '6':
                if not condition.max_val.isdigit():
                    formula = condition.max_val
                    vars_max_val = get_vars_formula(formula)
                    for var_max_val in vars_max_val:
                        formula = formula.replace(str(var_max_val),
                                                  str(ScResults.objects.filter(var_title=var_max_val)[
                                                          0].value))
                    digit_max_val = formula
                    max_val = eval(formula)
                else:
                    max_val = float(condition.max_val)
                    digit_max_val = max_val
                if not condition.min_val.isdigit():
                    formula = condition.min_val
                    vars_min_val = get_vars_formula(formula)
                    for var_min_val in vars_min_val:
                        formula = formula.replace(str(var_min_val),
                                                  str(ScResults.objects.filter(var_title=var_min_val)[
                                                          0].value))
                    digit_min_val = formula
                    min_val = eval(formula)
                else:
                    min_val = float(condition.min_val)
                    digit_min_val = min_val
                val_formula = digit_formula + ' in ' + '[' + str(digit_min_val) + ' ; ' + str(
                    digit_max_val) + '] ?'
                text_formula = condition.formula + ' in ' + '[' + str(condition.min_val) + ' ; ' + str(
                    condition.max_val) + '] ?'
                result_formula = str(eval(str(digit_formula))) + ' in ' + '[' + str(
                    eval(str(digit_min_val))) + ' ; ' + str(eval(str(digit_max_val))) + '] ?'
                bool_result = bool(max_val >= result >= min_val)
                if not bool_result and condition.display_method == 'Text+Siren':
                    ids_for_signal_alarm.append(condition.cond_id)
                result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=val_formula,
                                                   bool_result=bool_result, text_formula=text_formula,
                                                   val_result=result, result_formula=result_formula,
                                                   time_calc=(datetime.now(tz=timezone.utc)))
                result_for_db.save()
            if condition.cond_type == '2' or condition.cond_type == '3' or condition.cond_type == '4' or condition.cond_type == '5':
                if not condition.limit_val.isdigit():
                    formula = condition.limit_val
                    vars_limit_val = get_vars_formula(formula)
                    for var_limit_val in vars_limit_val:
                        formula = formula.replace(str(var_limit_val),
                                                  str(ScResults.objects.filter(var_title=var_limit_val)[
                                                          0].value))
                    digit_limit_val = formula
                    limit_val = eval(formula)
                else:
                    limit_val = float(condition.limit_val)
                    digit_limit_val = limit_val
                if condition.cond_type == '2':
                    val_formula = digit_formula + '<' + str(digit_limit_val)
                    text_formula = condition.formula + '<' + condition.limit_val
                    result_formula = str(eval(str(digit_formula))) + '<' + str(eval(str(digit_limit_val)))
                    bool_result = bool(result < limit_val)
                    if not bool_result and condition.display_method == 'Text+Siren':
                        ids_for_signal_alarm.append(condition.cond_id)
                if condition.cond_type == '3':
                    val_formula = digit_formula + '>' + str(digit_limit_val)
                    text_formula = condition.formula + '>' + condition.limit_val
                    result_formula = str(eval(str(digit_formula))) + '>' + str(eval(str(digit_limit_val)))
                    bool_result = bool(result > limit_val)
                    if not bool_result and condition.display_method == 'Text+Siren':
                        ids_for_signal_alarm.append(condition.cond_id)
                if condition.cond_type == '4':
                    val_formula = digit_formula + '>=' + str(digit_limit_val)
                    text_formula = condition.formula + '>=' + condition.limit_val
                    result_formula = str(eval(str(digit_formula))) + '>=' + str(eval(str(digit_limit_val)))
                    bool_result = bool(result >= limit_val)
                    if not bool_result and condition.display_method == 'Text+Siren':
                        ids_for_signal_alarm.append(condition.cond_id)
                if condition.cond_type == '5':
                    val_formula = digit_formula + '<=' + str(digit_limit_val)
                    text_formula = condition.formula + '<=' + condition.limit_val
                    result_formula = str(eval(str(digit_formula))) + '<=' + str(eval(str(digit_limit_val)))
                    bool_result = bool(result <= limit_val)
                    if not bool_result and condition.display_method == 'Text+Siren':
                        ids_for_signal_alarm.append(condition.cond_id)
                result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=val_formula,
                                                   bool_result=bool_result, text_formula=text_formula,
                                                   val_result=result, result_formula=result_formula,
                                                   time_calc=(datetime.now(tz=timezone.utc)))
                result_for_db.save()
    return ids_for_signal_alarm


def signal_alarm(siren_ids, connection, cursor):
    query_for_input_messages = "insert into messages (user, process, loglevel, topic, subject, attachment, alarm) values(%s, %s, %s, %s, %s, %s, %s)"
    query_for_get_id = 'select id,time from messages where user=%s and subject=%s order by time limit 1'
    query_for_input_attachment = 'insert into attachments (message_id, name, size, type, value, inline) values (%s, %s, %s, %s, %s, %s)'
    for siren_id in siren_ids:
        condition = ScConditions.objects.get(cond_id=siren_id)
        condition_result = ScConditionsResult.objects.get(cond_id=siren_id)
        if condition.isalert == 1:
            if int(condition.alert_interval) < (condition_result.time_calc - condition.time_create_or_alert).total_seconds():
                print('Время расчета'+str(condition_result.time_calc))
                print('Время создания или сигнала'+str(condition.time_create_or_alert))
                print('Разница времен'+str((condition_result.time_calc - condition.time_create_or_alert).total_seconds()))
                subject = '<!-- {sadness sound} --> Signal Alert! Condition:' + condition.comment + ' не выполнено!'
                username = condition.user
                # Создадим JSON с информацией
                info = {"The condition was calculated in": (condition_result.time_calc + timedelta(hours=7)),
                        "Result formula": condition_result.result_formula,
                        "Value Formula": condition_result.val_formula, "Text Formula": condition_result.text_formula}
                value_json = json.dumps(info, default=str)
                size = len(info)
                # Посчитаем длину json
                # Записали в messages
                cursor.execute(query_for_input_messages, (username, 'sam_sc', 'w', 'user-alarm', subject, 'y', 'y'))
                connection.commit()
                # Получили id нашего message
                cursor.execute(query_for_get_id, (username, subject))
                message = cursor.fetchone()
                # Записали attachment
                cursor.execute(query_for_input_attachment,
                               (message['id'], 'alarm.json', str(size), 'application/json; charset=utf8', value_json,
                                'y'))
                connection.commit()

                condition.time_create_or_alert = datetime.now(tz=timezone.utc)
                condition.save()
        if condition.isalert == 0:
            # закидываем в журнальчик
            subject = '<!-- {sadness sound} --> Signal Alert! Condition:' + condition.comment + ' не выполнено!'
            username = condition.user
            # Создадим JSON с информацией
            info = {"The condition was calculated in": (condition_result.time_calc + timedelta(hours=7)),
                    "Result formula": condition_result.result_formula,
                    "Value Formula": condition_result.val_formula, "Text Formula": condition_result.text_formula}
            value_json = json.dumps(info, default=str)
            size = len(info)
            # Посчитаем длину json
            # Записали в messages
            cursor.execute(query_for_input_messages, (username, 'sam_sc', 'w', 'user-alarm', subject, 'y', 'y'))
            connection.commit()
            # Получили id нашего message
            cursor.execute(query_for_get_id, (username, subject))
            message = cursor.fetchone()
            # Записали attachment
            cursor.execute(query_for_input_attachment,
                           (message['id'], 'alarm.json', str(size), 'application/json; charset=utf8', value_json,
                            'y'))
            connection.commit()

            condition.time_create_or_alert = datetime.now(tz=timezone.utc)
            condition.isalert = 1
            condition.save()


'''Запускается одна задача, которая выполняется постоянно, каждые 5 секунд и проверяет все условия и если нужно - записывает в log журнал'''


def test():
    cur, con = get_connection_journal_db()
    t_update = 5  # Время обновления в секундах
    t_end = time.time() + 60
    signal_alarm(update_condition_results(), con, cur)
    # while time.time() < t_end:
    #     t_start = time.time()
    #     signal_alarm(update_condition_results(), con, cur)
    #     # update_condition_results()
    #     t_res = t_update - (time.time() - t_start)
    #     if t_res > 0:
    #         time.sleep(t_res)
    close_connection_journal_db(cur, con)
