from .models import ScConditionsResult
from .models import ScUsers, ScPaths, ScresultsTest, ScConditions
from datetime import datetime, timedelta
import time
import re


def get_vars_formula(formula):
    x = re.findall(
        "(([A-Za-z0-9_]+):((?:\\.|[A-Za-z0-9_.\-\/])+):([A-Za-z0-9_]+)(?:\(([+-]?\d+)([a-z]+)(?:,([+-]?\d+)([a-z]+))\))?)",
        formula)
    vars_formula = list()
    for i in range(len(x)):
        vars_formula.append(x[i][0])
    return vars_formula


def update_condition_results():
    try:
        global bool_result
        '''Время волшебства'''
        data = ScConditions.objects.all()
        for condition in data:
            formula = condition.formula
            vars_formula = get_vars_formula(formula)
            empty_values = list()
            for var_formula in vars_formula:
                cur_time = time.time()
                formula = formula.replace(str(var_formula),
                                          str(ScresultsTest.objects.filter(var_title=var_formula)[0].value))
                if str(ScresultsTest.objects.filter(var_title=var_formula)[0].comment) == 'Empty':
                    empty_values.append(str(ScresultsTest.objects.filter(var_title=var_formula)[0].var_title))
            digit_formula = formula
            if empty_values:
                result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=formula,
                                                   empty_values=str(empty_values), text_formula=condition.formula,
                                                   time_calc=(datetime.now()) + timedelta(hours=7))
                result_for_db.save()
            else:
                result = eval(digit_formula)
                if condition.cond_type == '1':
                    result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=formula,
                                                       val_result=result,
                                                       text_formula=condition.formula,
                                                       time_calc=(datetime.now()) + timedelta(hours=7))
                    result_for_db.save()
                if condition.cond_type == '6':
                    if not condition.max_val.isdigit():
                        formula = condition.max_val
                        vars_max_val = get_vars_formula(formula)
                        for var_max_val in vars_max_val:
                            formula = formula.replace(str(var_max_val),
                                                      str(ScresultsTest.objects.filter(var_title=var_max_val)[
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
                                                      str(ScresultsTest.objects.filter(var_title=var_min_val)[
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
                    result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=val_formula,
                                                       bool_result=bool_result, text_formula=text_formula,
                                                       val_result=result, result_formula=result_formula,
                                                       time_calc=(datetime.now()) + timedelta(hours=7))
                    result_for_db.save()
                if condition.cond_type == '2' or condition.cond_type == '3' or condition.cond_type == '4' or condition.cond_type == '5':
                    if not condition.limit_val.isdigit():
                        formula = condition.limit_val
                        vars_limit_val = get_vars_formula(formula)
                        for var_limit_val in vars_limit_val:
                            formula = formula.replace(str(var_limit_val),
                                                      str(ScresultsTest.objects.filter(var_title=var_limit_val)[
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
                    if condition.cond_type == '3':
                        val_formula = digit_formula + '>' + str(digit_limit_val)
                        text_formula = condition.formula + '>' + condition.limit_val
                        result_formula = str(eval(str(digit_formula))) + '>' + str(eval(str(digit_limit_val)))
                        bool_result = bool(result > limit_val)
                    if condition.cond_type == '4':
                        val_formula = digit_formula + '>=' + str(digit_limit_val)
                        text_formula = condition.formula + '>=' + condition.limit_val
                        result_formula = str(eval(str(digit_formula))) + '>=' + str(eval(str(digit_limit_val)))
                        bool_result = bool(result >= limit_val)
                    if condition.cond_type == '5':
                        val_formula = digit_formula + '<=' + str(digit_limit_val)
                        text_formula = condition.formula + '<=' + condition.limit_val
                        result_formula = str(eval(str(digit_formula))) + '<=' + str(eval(str(digit_limit_val)))
                        bool_result = bool(result <= limit_val)
                    result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=val_formula,
                                                       bool_result=bool_result, text_formula=text_formula,
                                                       val_result=result, result_formula=result_formula,
                                                       time_calc=(datetime.now()) + timedelta(hours=7))
                    time_for_calc = time.time() - cur_time
                    cur_time = time.time()
                    result_for_db.save()
                    time_for_db = time.time() - cur_time
        print('done')
    except:
        print('gg')


def test():
    t_update = 5  # Время обновления в секундах
    t_end = time.time() + 60
    while time.time() < t_end:
        t_start = time.time()
        update_condition_results()
        t_res = t_update - (time.time() - t_start)
        if t_res > 0:
            time.sleep(t_res)

