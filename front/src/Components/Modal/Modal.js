import React from 'react';
import crossSVG from '../../Assets/icon/cross.svg';
import './Modal.css';

function Modal({ title, children, isOpen, onClose }) {
    const modalSheet = React.useRef(null);

    React.useEffect(() => {
        if (isOpen) {
            modalSheet.current.classList.remove('close')
            modalSheet.current.classList.add('open');
        }
        else {
            modalSheet.current.classList.remove('open')
            modalSheet.current.classList.add('close');
        }
    }, [isOpen])

    return (
        <div className='modal-sheet' ref={modalSheet}>
            <dialog>
                <div className='modal-header'>
                    <div></div>
                    <span className='modal-title'>{title}</span>
                    <button className='close-btn' onClick={() => onClose()}>
                        <img alt='cross' src={crossSVG}></img>
                    </button>
                </div>
                <div className='modal-content'>
                    {children}
                </div>
            </dialog>
        </div>
    );
}

export default Modal;