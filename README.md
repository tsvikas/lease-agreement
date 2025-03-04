# חוזה שכירות מומלץ
מבוסס על החוזה המומלץ של עיריית תל אביב, עם שינויים.
לפירוט השינויים ראה [כאן](https://github.com/tsvikas/lease-agreement-text/commits/main/)

כל הזכויות לחוזה המקורי שמורות לבעלי הזכויות המקוריים, ככל שיש כאלה.

## שימוש בסיסי
באמצעות הקוד המצורף אפשר למלא את החוזה בפרטי הצדדים.
לחילופין, מסופקת [גירסה ריקה של החוזה](output/lease-blank.md).

מומלץ להעתיק אותה (כפתור Copy raw file), ולהדביק אותה לתוך Google Doc (לחיצה ימנית, Paste from Markdown).

(דורש לעשות Tools, Preferences, Enable Markdown)

## הסרת אחריות
השימוש בחוזה השכירות הינו באחריותם הבלעדית של הצדדים לחוזה.
מובהר כי אין כל אחריות בנוגע ליישום הוראות החוזה בין הצדדים או לפרשנותו.

אין בחוזה השכירות ובחומרי ההסבר הנלווים כדי להוות ייעוץ משפטי או תחליף לייעוץ משפטי אצל עורך דין.

הטקסט להלן נועד לצורכי מידע בלבד ואינו מהווה ייעוץ משפטי, התחייבות או מסמך מחייב מכל סוג שהוא.
מומלץ להיוועץ בעורך דין מוסמך או מומחה מתאים לפני הסתמכות על תוכן זה או שימוש בו.
הכותב אינו נושא באחריות לשום נזק או הפסד שעלול להיגרם כתוצאה משימוש בתוכן זה.

## Usage
Create a new Markdown with your personal data with
```
poetry install
poetry run src/render.py -i <path to input toml> -o <path to output file>
```
or use the [pre-made blank lease](output/lease-blank.md)

The markdown can be viewed or edited with various editors.
To use Google Docs, see [this](https://support.google.com/docs/answer/12014036):
you'll need to turn markdown on, then "Paste from Markdown"

## מקורות
### עיריית תל אביב
[חוזה שכירות מומלץ](https://www.tel-aviv.gov.il/Residents/Assets/Pages/rent.aspx)

**גירסה 1**:
[חוזה מומלץ עם טיפים](https://www.tel-aviv.gov.il/Residents/Assets/Pages/hoze.aspx)

**גירסת 2016**:
[Word](https://www.tel-aviv.gov.il/Forms/חוזה%20שכירות%20עירוני%20מומלץ%20-%20עברית%20-%20קובץ%20word.docx)
[PDF](https://www.tel-aviv.gov.il/Forms/חוזה%20שכירות%20מומלץ.pdf)

**גירסת 2023**:
[Word](https://www.tel-aviv.gov.il/Forms/חוזה%20עירוני%20מומלץ%20-%20עדכון%202023.docx)
[PDF](https://www.tel-aviv.gov.il/Forms/חוזה%20עירוני%20מומלץ%20-%20עדכון%202023.pdf)

**כתב ערבות ושטר חוב**:
[PDF](https://www.tel-aviv.gov.il/Forms/כתב%20ערבות%20ושטר%20חוב.pdf)

### קוד השכירות
**גירסה 1**:
[Word](https://docs.wixstatic.com/ugd/e716da_f38c159dc8454a7d800ba5737b9ddc14.docx?dn=נוסח%20סופי%20חוזה%20מומלץ%20קוד%20השכירות.docx)
