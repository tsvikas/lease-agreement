def verbal_number_3(i: int, male):
    if not 0 <= i < 1000:
        raise ValueError("number must be 3 digits")
    female_n = "אפס אחת שתים שלוש ארבע חמש שש שבע שמונה תשע עשר".split()
    male_n = "אפס אחד שנים שלושה ארבעה חמישה שישה שבעה שמונה תשעה עשרה".split()
    res = []
    # 100
    h = i // 100
    if h == 1:
        res += ["מאה"]
    elif h == 2:
        res += ["מאתיים"]
    elif h > 2:
        res += [female_n[h] + "־מאות"]
    i = i - h * 100
    # 10
    t = i // 10
    if i >= 20:
        res += ["עשרים שלושים ארבעים חמישים שישים שבעים שמונים תשעים".split()[t - 2]]
        i = i - t * 10
    if i > 10:
        if male:
            res += [male_n[i - 10] + "־עשר"]
        else:
            res += [female_n[i - 10] + "־עשרה"]
    elif i > 0:
        if male:
            res += [male_n[i]]
        else:
            res += [female_n[i]]

    return res


def join(res):
    if not res:
        raise ValueError("empty res")
    if len(res) == 1:
        return res[0]
    return ", ".join(res[:-1]) + " ו" + res[-1]


def verbal_number(i: int, male=False):
    res = []
    if i < 0:
        res += ["מינוס"]
        i = -i
    if not i < 1_000_000:
        raise NotImplementedError("only support numbers up to 1000000")
    t, r = divmod(i, 1_000)
    if t > 10:
        res += [join(verbal_number_3(t, male=True)) + " אלף"]
    elif t >= 3:
        res += ["שלושת ארבעת חמשת ששת שבעת שמונת תשעת עשרת".split()[t - 3] + "־אלפים"]
    elif t == 2:
        res += ["אלפיים"]
    elif t == 1:
        res += ["אלף"]

    if r:
        res += verbal_number_3(r, male)

    if not res:
        return "אפס"
    return join(res)
