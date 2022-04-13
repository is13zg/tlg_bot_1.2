import logging
from aiogram.utils import executor
from create_bot import dp
from my_filters import IsAdmin, IsNotAdmin, IsGod
import init_data
from handlers import censor_handlers, client, admin

# run long-polling
if __name__ == "__main__":
    # log level
    logging.basicConfig(
        level=logging.WARNING,
        filename="mylog.log",
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%D_%H:%M:%S')

    # bot init
    init_data.init_data()
    dp.bind_filter(IsAdmin)
    dp.bind_filter(IsNotAdmin)
    dp.bind_filter(IsGod)

    client.register_handlers_client(dp)
    admin.register_handlers_admin(dp)
    censor_handlers.register_handlers_censor_handlers(dp)

    executor.start_polling(dp, skip_updates=True)
