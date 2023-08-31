def getMailContent(code):
    return """Hello,<br>
        Thank you for registering.<br><br>

        The Educational highlights and English writing learning aids can help you study more efficiently.<br>
        I hope you like it, and use it a lot.<br><br>

        If you encounter any problems, you can always write to us, <br>
        we are more than happy to improve and deal with it<br><br>

        <strong>您的驗證碼是 {}，請在10分鐘內在網站上輸入驗證碼以完成驗證。</strong><br><br>
        Regards,<br>
        Study Savvy
        """.format(code)