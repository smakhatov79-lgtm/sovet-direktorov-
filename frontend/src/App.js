import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [directors, setDirectors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/directors/")
      .then(res => {
        setDirectors(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div style={{padding: 30, fontFamily: 'Arial', background: '#f5f5f5', minHeight: '100vh'}}>
      <h1 style={{color: '#1a1a1a'}}>Совет Директоров - Портал</h1>
      <div style={{background: 'white', padding: 20, borderRadius: 10, marginTop: 20}}>
        <h2>Директора ({directors.length})</h2>
        {loading ? <p>Загрузка...</p> : 
          directors.length === 0 ? <p>Нет директоров. Создай через /docs</p> :
          directors.map(d => (
            <div key={d.id} style={{padding: '10px 0', borderBottom: '1px solid #eee'}}>
              - {d.fio} ({d.position})
            </div>
          ))
        }
      </div>
      <p style={{marginTop: 20, color: 'green'}}>✅ Фронт (3000) подключен к Бэку (8000)</p>
    </div>
  );
}
export default App;