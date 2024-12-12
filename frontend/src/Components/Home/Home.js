import React, { useEffect, useState } from 'react';
import { API_URL } from '../../config';
import Alert from '../Alert/Alert';
import Footer from '../Footer/Footer';
import Modal from '../Modal/Modal';
import './Home.css';


function Home() {
  const [inviteModalState, inviteModalSetState] = useState(false);
  const [testModalState, testModalSetState] = useState(false);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/users/ref/link`, {
      headers: { 'Authorization': `Bearer ${btoa(window.Telegram.WebApp.initData)}` }
    })
      .then(response => response.json())
      .then(data => {
        console.log(data)
      })
  }, []);

  function copyLink() {
    inviteModalSetState(false);

    var alert = React.createElement(
      Alert, { text: 'Copied' }
    )

    setAlerts([...alerts, alert]);
  }

  window.Telegram.WebApp.expand();
  const initDataUnsafe = window.Telegram.WebApp.initDataUnsafe

  return (
    <div>
      <div className='page home-page'>
        {alerts.map((alert, idx) => (
          <div key={`alert item ${idx}`}>
            {alert}
          </div>
        ))}
        <div className='page-head'>
          <div className='avatar-wrapper'>
            <img alt='avatar' src={initDataUnsafe.user.photo_url} className='avatar'></img>
          </div>
          <div className='username'>{initDataUnsafe.user.username}</div>

          <div style={{ "fontSize": "20px", "margin": "auto", "marginBlock": "50px", "width": "300px" }}>
            <button className='kit-button' onClick={() => testModalSetState(true)}> Test Modal </button>
          </div>
        </div>
        <div className='invite-button-wrapper'>
          <button className='kit-button' onClick={() => inviteModalSetState(true)}>
            <div className='label'>Invite a fren</div>
          </button>
        </div>
      </div>
      <Footer active='Home' />

      <Modal title="Invite a fren" isOpen={inviteModalState} onClose={() => inviteModalSetState(false)}>
        <div className='content-inner'>
          <button className='kit-button'>
            <div className='label'>Send</div>
          </button>
          <button className='kit-button' onClick={() => copyLink()}>
            <div className='label'>Copy Link</div>
          </button>
        </div>
      </Modal>

      <Modal title="Test Info" isOpen={testModalState} onClose={() => testModalSetState(false)}>
        <div className='content-inner'>
          <h4 style={{ textAlign: 'center' }}>Test modal</h4>
        </div>
      </Modal>
    </div>
  );
}
export default Home;