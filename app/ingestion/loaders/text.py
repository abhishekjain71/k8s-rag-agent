import logfire

def parse_text(file_paht: str):
    """ parse plain text
    """
    with logfire.span("Text parsing",filename=file_paht):
        try:
            with open(file_paht, 'r',encoding='utf-8',errors='ignore') as f:
                return f.read()
            
        except Exception as e:
            logfire.error(f"Text parse Failed {e}")
            raise e