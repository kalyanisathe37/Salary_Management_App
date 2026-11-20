import { useEffect, useState } from "react";
import { Layout, Tabs, Table, Input, Select, Button, Space, Popconfirm, message } from "antd";
import {
  getEmployees,
  createEmployee,
  updateEmployee,
  deleteEmployee,
  getInsightsByCountry,
  getInsightsByJobTitle,
} from "./api";
import EmployeeForm from "./EmployeeForm";

const { Header, Content } = Layout;

const COUNTRIES = ["India", "USA", "UK", "Germany", "Singapore"];

function EmployeesTab() {
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [country, setCountry] = useState();
  const [loading, setLoading] = useState(false);
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      const res = await getEmployees({ page, search, country });
      setData(res.data.results);
      setTotal(res.data.count);
    } catch {
      message.error("Failed to load employees");
    }
    setLoading(false);
  };

  useEffect(() => { load(); }, [page, search, country]);

  const onDelete = async (id) => {
    await deleteEmployee(id);
    message.success("Deleted");
    load();
  };

  const onSave = async (values) => {
    try {
      if (editing) {
        await updateEmployee(editing.id, values);
        message.success("Updated");
      } else {
        await createEmployee(values);
        message.success("Added");
      }
      setFormOpen(false);
      load();
    } catch (e) {
      const err = e.response?.data;
      message.error(err ? JSON.stringify(err) : "Save failed");
    }
  };

  const columns = [
    { title: "Name", dataIndex: "full_name" },
    { title: "Email", dataIndex: "email" },
    { title: "Job Title", dataIndex: "job_title" },
    { title: "Country", dataIndex: "country" },
    { title: "Salary", render: (_, r) => `${r.currency} ${Number(r.salary).toLocaleString()}` },
    {
      title: "Action",
      render: (_, r) => (
        <Space>
          <Button size="small" onClick={() => { setEditing(r); setFormOpen(true); }}>
            Edit
          </Button>
          <Popconfirm title="Delete this employee?" onConfirm={() => onDelete(r.id)}>
            <Button danger size="small">Delete</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <>
      <Space style={{ marginBottom: 16 }}>
        <Input.Search
          placeholder="Search name or email"
          allowClear
          onSearch={(v) => { setPage(1); setSearch(v); }}
          style={{ width: 260 }}
        />
        <Select
          placeholder="Country"
          allowClear
          style={{ width: 160 }}
          options={COUNTRIES.map((c) => ({ value: c, label: c }))}
          onChange={(v) => { setPage(1); setCountry(v); }}
        />
        <Button type="primary" onClick={() => { setEditing(null); setFormOpen(true); }}>
          Add Employee
        </Button>
      </Space>
      <Table
        rowKey="id"
        columns={columns}
        dataSource={data}
        loading={loading}
        pagination={{ current: page, total, pageSize: 50, showSizeChanger: false, onChange: setPage }}
      />
      <EmployeeForm
        open={formOpen}
        employee={editing}
        onSubmit={onSave}
        onCancel={() => setFormOpen(false)}
      />
    </>
  );
}

function InsightsTab() {
  const [byCountry, setByCountry] = useState([]);
  const [byTitle, setByTitle] = useState([]);

  useEffect(() => {
    getInsightsByCountry().then((r) => setByCountry(r.data));
    getInsightsByJobTitle().then((r) => setByTitle(r.data));
  }, []);

  const cols = (key, label) => [
    { title: label, dataIndex: key },
    { title: "Currency", dataIndex: "currency" },
    { title: "Headcount", dataIndex: "count" },
    { title: "Min", dataIndex: "min", render: (v) => v.toLocaleString() },
    { title: "Avg", dataIndex: "avg", render: (v) => v.toLocaleString() },
    { title: "Median", dataIndex: "median", render: (v) => v.toLocaleString() },
    { title: "Max", dataIndex: "max", render: (v) => v.toLocaleString() },
  ];

  return (
    <>
      <h3>By Country</h3>
      <Table
        rowKey={(r) => r.country + r.currency}
        columns={cols("country", "Country")}
        dataSource={byCountry}
        pagination={false}
      />
      <h3 style={{ marginTop: 24 }}>By Job Title</h3>
      <Table
        rowKey={(r) => r.job_title + r.currency}
        columns={cols("job_title", "Job Title")}
        dataSource={byTitle}
        pagination={false}
      />
    </>
  );
}

export default function App() {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header style={{ color: "white", fontSize: 20 }}>ACME Salary Management</Header>
      <Content style={{ padding: 24 }}>
        <Tabs
          items={[
            { key: "1", label: "Employees", children: <EmployeesTab /> },
            { key: "2", label: "Insights", children: <InsightsTab /> },
          ]}
        />
      </Content>
    </Layout>
  );
}