\# School Management System — Role-Based Access (RBAC)



\## 👥 User Roles (Groups)

\- \*\*Admin\*\*: Full access to manage users and data.

\- \*\*Teacher\*\*: Can view, create, and edit subjects.

\- \*\*Student\*\*: Can view subjects and grades.

\- \*\*Parent\*\*: Can view student's performance.



\## 🔐 Permissions

Custom permissions defined on the `Subject` model:

\- `can\_view`: View subject info

\- `can\_create`: Add new subjects

\- `can\_edit`: Edit subjects

\- `can\_delete`: Delete subjects



