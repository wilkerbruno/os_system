[2026-06-11 01:15:22 +0000] [7] [INFO] Starting gunicorn 22.0.0
[2026-06-11 01:15:22 +0000] [7] [INFO] Listening at: http://0.0.0.0:80 (7)
[2026-06-11 01:15:22 +0000] [7] [INFO] Using worker: sync
[2026-06-11 01:15:22 +0000] [8] [INFO] Booting worker with pid: 8
[2026-06-11 01:15:22 +0000] [9] [INFO] Booting worker with pid: 9
⚠️  MySQL indisponível ((1045, "Access denied for user 'mysql'@'2.25.131.174' (using password: YES)"))
⚠️  Usando SQLite local: /app/techos_local.db
   Para usar MySQL, libere o IP da sua máquina no EasyPanel.
✅ Tabelas OK
⚠️  Seed: name 'User' is not defined
10.11.0.4 - - [11/Jun/2026:01:15:37 +0000] "GET / HTTP/1.1" 200 94674 "https://2.25.131.174/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
10.11.0.4 - - [11/Jun/2026:01:15:38 +0000] "GET /favicon.ico HTTP/1.1" 404 207 "https://divisions-os-system.lcgx8u.easypanel.host/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
[2026-06-11 01:18:10,795] ERROR in app: Exception on /api/auth/login [POST]
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlite3.OperationalError: no such table: user

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask_cors/extension.py", line 178, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 880, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 865, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app.py", line 481, in login
    ).first()
      ^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2766, in first
    return self.limit(1)._iter().first()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2864, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2372, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2270, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
    return meth(
           ^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2365, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.name AS user_name, user.username AS user_username, user.email AS user_email, user.password_hash AS user_password_hash, user.role AS user_role, user.technician_id AS user_technician_id, user.store_id AS user_store_id, user.first_login AS user_first_login, user.active AS user_active, user.created_at AS user_created_at 
FROM user 
WHERE (user.username = ? OR user.email = ?) AND user.active = 1
 LIMIT ? OFFSET ?]
[parameters: ('wilker', 'wilker', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
⚠️  MySQL indisponível ((1045, "Access denied for user 'mysql'@'2.25.131.174' (using password: YES)"))
⚠️  Usando SQLite local: /app/techos_local.db
   Para usar MySQL, libere o IP da sua máquina no EasyPanel.
✅ Tabelas OK
⚠️  Seed: name 'User' is not defined
10.11.0.4 - - [11/Jun/2026:01:18:10 +0000] "POST /api/auth/login HTTP/1.1" 500 265 "https://divisions-os-system.lcgx8u.easypanel.host/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
[2026-06-11 01:18:13,186] ERROR in app: Exception on /api/auth/login [POST]
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlite3.OperationalError: no such table: user

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask_cors/extension.py", line 178, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 880, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 865, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app.py", line 481, in login
    ).first()
      ^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2766, in first
    return self.limit(1)._iter().first()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2864, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
[2026-06-11 02:13:47 +0000] [7] [INFO] Starting gunicorn 22.0.0
[2026-06-11 02:13:47 +0000] [7] [INFO] Listening at: http://0.0.0.0:80 (7)
[2026-06-11 02:13:47 +0000] [7] [INFO] Using worker: sync
[2026-06-11 02:13:47 +0000] [8] [INFO] Booting worker with pid: 8
[2026-06-11 02:13:47 +0000] [9] [INFO] Booting worker with pid: 9
⚠️  MySQL indisponível ((2003, "Can't connect to MySQL server on '2.25.131.174' (timed out)"))
⚠️  Usando SQLite local: /app/techos_local.db
   Para usar MySQL, verifique a conexão com 2.25.131.174:3409
✅ Tabelas OK
⚠️  Seed: name 'User' is not defined
10.11.0.4 - - [11/Jun/2026:02:14:04 +0000] "GET / HTTP/1.1" 200 94674 "https://2.25.131.174/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
[2026-06-11 02:14:12,909] ERROR in app: Exception on /api/auth/login [POST]
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlite3.OperationalError: no such table: user

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask_cors/extension.py", line 178, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 880, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 865, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app.py", line 480, in login
    ).first()
      ^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2766, in first
    return self.limit(1)._iter().first()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2864, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2372, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2270, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
    return meth(
           ^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2365, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.name AS user_name, user.username AS user_username, user.email AS user_email, user.password_hash AS user_password_hash, user.role AS user_role, user.technician_id AS user_technician_id, user.store_id AS user_store_id, user.first_login AS user_first_login, user.active AS user_active, user.created_at AS user_created_at 
FROM user 
WHERE (user.username = ? OR user.email = ?) AND user.active = 1
 LIMIT ? OFFSET ?]
[parameters: ('admin', 'admin', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
10.11.0.4 - - [11/Jun/2026:02:14:12 +0000] "POST /api/auth/login HTTP/1.1" 500 265 "https://divisions-os-system.lcgx8u.easypanel.host/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
[2026-06-11 02:14:14,977] ERROR in app: Exception on /api/auth/login [POST]
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlite3.OperationalError: no such table: user

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask_cors/extension.py", line 178, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 880, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 865, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app.py", line 480, in login
    ).first()
      ^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2766, in first
    return self.limit(1)._iter().first()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2864, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2372, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2270, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
    return meth(
           ^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2365, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.name AS user_name, user.username AS user_username, user.email AS user_email, user.password_hash AS user_password_hash, user.role AS user_role, user.technician_id AS user_technician_id, user.store_id AS user_store_id, user.first_login AS user_first_login, user.active AS user_active, user.created_at AS user_created_at 
FROM user 
WHERE (user.username = ? OR user.email = ?) AND user.active = 1
 LIMIT ? OFFSET ?]
[parameters: ('admin', 'admin', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
10.11.0.4 - - [11/Jun/2026:02:14:14 +0000] "POST /api/auth/login HTTP/1.1" 500 265 "https://divisions-os-system.lcgx8u.easypanel.host/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
[2026-06-11 02:14:16,847] ERROR in app: Exception on /api/auth/login [POST]
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlite3.OperationalError: no such table: user

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask_cors/extension.py", line 178, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 880, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 865, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app.py", line 480, in login
    ).first()
      ^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2766, in first
    return self.limit(1)._iter().first()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2864, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2372, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2270, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
    return meth(
           ^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2365, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.name AS user_name, user.username AS user_username, user.email AS user_email, user.password_hash AS user_password_hash, user.role AS user_role, user.technician_id AS user_technician_id, user.store_id AS user_store_id, user.first_login AS user_first_login, user.active AS user_active, user.created_at AS user_created_at 
FROM user 
WHERE (user.username = ? OR user.email = ?) AND user.active = 1
 LIMIT ? OFFSET ?]
[parameters: ('admin', 'admin', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
10.11.0.4 - - [11/Jun/2026:02:14:16 +0000] "POST /api/auth/login HTTP/1.1" 500 265 "https://divisions-os-system.lcgx8u.easypanel.host/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
[2026-06-11 12:54:06,751] ERROR in app: Exception on /api/auth/login [POST]
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlite3.OperationalError: no such table: user

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask_cors/extension.py", line 178, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 880, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 865, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app.py", line 480, in login
    ).first()
      ^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2766, in first
    return self.limit(1)._iter().first()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2864, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2372, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2270, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
    return meth(
           ^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2365, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.name AS user_name, user.username AS user_username, user.email AS user_email, user.password_hash AS user_password_hash, user.role AS user_role, user.technician_id AS user_technician_id, user.store_id AS user_store_id, user.first_login AS user_first_login, user.active AS user_active, user.created_at AS user_created_at 
FROM user 
WHERE (user.username = ? OR user.email = ?) AND user.active = 1
 LIMIT ? OFFSET ?]
[parameters: ('admin', 'admin', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
⚠️  MySQL indisponível ((2003, "Can't connect to MySQL server on '2.25.131.174' (timed out)"))
⚠️  Usando SQLite local: /app/techos_local.db
   Para usar MySQL, verifique a conexão com 2.25.131.174:3409
✅ Tabelas OK
⚠️  Seed: name 'User' is not defined
10.11.0.4 - - [11/Jun/2026:12:54:06 +0000] "POST /api/auth/login HTTP/1.1" 500 265 "https://divisions-os-system.lcgx8u.easypanel.host/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
[2026-06-11 12:54:07,113] ERROR in app: Exception on /api/auth/login [POST]
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlite3.OperationalError: no such table: user

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask_cors/extension.py", line 178, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 880, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 865, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app.py", line 480, in login
    ).first()
      ^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2766, in first
    return self.limit(1)._iter().first()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2864, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2372, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2270, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
    return meth(
           ^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2365, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.name AS user_name, user.username AS user_username, user.email AS user_email, user.password_hash AS user_password_hash, user.role AS user_role, user.technician_id AS user_technician_id, user.store_id AS user_store_id, user.first_login AS user_first_login, user.active AS user_active, user.created_at AS user_created_at 
FROM user 
WHERE (user.username = ? OR user.email = ?) AND user.active = 1
 LIMIT ? OFFSET ?]
[parameters: ('admin', 'admin', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
10.11.0.4 - - [11/Jun/2026:12:54:07 +0000] "POST /api/auth/login HTTP/1.1" 500 265 "https://divisions-os-system.lcgx8u.easypanel.host/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
