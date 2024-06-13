# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema


class LogSchema(BaseSchema):
    timestamp: str = Field(
        ...,
        title="タイムスタンプ",
        description="""
        QRコードのログを取得した日時を`isoformat`形式で指定してください。
        """,
    )
    userId: str = Field(
        ...,
        title="ユーザーID",
        description="ユーザーのIDを指定してください。S3に保存されるときにファイル名に使用されます。",
    )
    data: str = Field(
        ...,
        title="ログデータ",
        description="QRコードの`生のログデータ`を文字列で指定してください。`json`形式にする必要はありません。",
    )
