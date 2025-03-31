import React, { useState, useEffect } from "react";
import axios from "axios";

interface Workflow {
  id: number;
  name: string;
  description: string;
  category: string;
  tags: string[];
  platform: string;
}

const WorkflowList = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get("http://localhost:5000/workflows")
      .then((response: { data: React.SetStateAction<Workflow[]> }) => {
        setWorkflows(response.data);
        setLoading(false);
      })
      .catch((error: { message: React.SetStateAction<string | null> }) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <ul>
      {workflows.map((workflow) => (
        <li key={workflow.id}>
          <h2>{workflow.name}</h2>
          <p>{workflow.description}</p>
          <p>Category: {workflow.category}</p>
          <p>Tags: {workflow?.tags?.join(", ")}</p>
          <p>Platform: {workflow.platform}</p>
        </li>
      ))}
    </ul>
  );
};

export default WorkflowList;
